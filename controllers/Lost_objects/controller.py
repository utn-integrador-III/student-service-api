from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime
from bson import ObjectId
import pytz
import re

class LostObjectsListController(Resource):

    """
    Get all lost objects
    """
    
    route = '/lostObject'

    def get(self):
        try:
            lost_objects = LostObjectModel.get_all()

            if isinstance(lost_objects, dict) and "error" in lost_objects:
                return ServerResponse(data={}, message=lost_objects["error"], status=StatusCode.INTERNAL_SERVER_ERROR)

            if not lost_objects:  # If there are no lost objects
                return ServerResponse(data={}, message="No lost objects found", message_codes=NO_DATA, status=StatusCode.OK)

            def convert_object_id(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, ObjectId):
                            obj[key] = str(value)
                        elif isinstance(value, datetime):
                            obj[key] = value.isoformat()
                        elif isinstance(value, list):
                            obj[key] = [convert_object_id(item) for item in value]
                        elif isinstance(value, dict):
                            obj[key] = convert_object_id(value)
                return obj

            lost_objects = [convert_object_id(obj) for obj in lost_objects]

            return ServerResponse(data=lost_objects, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    def post(self):
        try:
            data = request.get_json()

            if not data.get("name"):
                return ServerResponse(message='Name is required', 
                                    message_code=LOST_OBJECTS_NAME_REQUIRED, status=StatusCode.BAD_REQUEST)

            if not data.get("description"):
                return ServerResponse(message='Description is required', 
                                    message_code=LOST_OBJECTS_DESCRIPTION_REQUIRED, status=StatusCode.BAD_REQUEST)
            
            user_email = data.get("user_email")
            if not user_email:
                return ServerResponse(message='User email is required', 
                                      message_code=LOST_OBJECTS_USER_EMAIL_REQUIRED, status=StatusCode.BAD_REQUEST)
            if not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr)$", user_email):
                return ServerResponse(message='Invalid email domain', 
                                      message_code=INVALID_EMAIL_DOMAIN, status=StatusCode.BAD_REQUEST)
            
            safekeepers = data.get("safekeeper")
            if not safekeepers or not isinstance(safekeepers, list):
                return ServerResponse(message='Safekeeper list is required', 
                                      message_code=LOST_OBJECTS_SAFEKEEPER_REQUIRED, status=StatusCode.BAD_REQUEST)
            
            validated_safekeepers = []
            for sk in safekeepers:
                email = sk.get("user_email")
                if not email or not re.match(r"^[\w\.-]+@utn\.ac\.cr$", email):  
                    return ServerResponse(message=f'Invalid email domain for safekeeper: {email}', 
                                          message_code=INVALID_EMAIL_DOMAIN, status=StatusCode.BAD_REQUEST)
                validated_safekeepers.append({"accepted": False, "user_email": email})
        
            data["status"] = "Pending"
            data["creation_date"] = datetime.now(pytz.timezone('America/Costa_Rica')).replace(tzinfo=None)
            data["attachment_path"] = '/lostObjects'
            data["claim_date"] = None
            data["claimer"] = ""
            data["safekeeper"] = validated_safekeepers
            data["user_email"] = user_email

            ordered_data = {
                "name": data["name"],
                "description": data["description"],
                "status": data["status"],
                "creation_date": data["creation_date"],
                "attachment_path": data["attachment_path"],
                "claim_date": data["claim_date"],
                "claimer": data["claimer"],
                "safekeeper": data["safekeeper"],
                "user_email": data["user_email"]
            }

            lost_object = LostObjectModel.create(ordered_data)
            return ServerResponse(lost_object.to_dict(), message="Lost_object successfully created", 
                                message_code=LOST_OBJECTS_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

