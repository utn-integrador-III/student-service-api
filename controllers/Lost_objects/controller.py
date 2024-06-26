from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime
from bson import ObjectId
from controllers.Lost_objects.parser import query_parser_save
import logging
import pytz
import re

class LostObjectsListController(Resource):
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

class LostObjectsDetailController(Resource):
    route = '/lostObject/<string:object_id>'

    def put(self, object_id):
        try:
            data = request.get_json()

            if not ObjectId.is_valid(object_id):
                return ServerResponse(message='Formato de ID inválido', message_code=INVALID_ID, status=StatusCode.BAD_REQUEST)

            update_data = {}
            if "name" in data:
                update_data["name"] = data["name"]
            if "description" in data:
                update_data["description"] = data["description"]
            if "status" in data:
                update_data["status"] = data["status"]
            if "attachment_path" in data:
                update_data["attachment_path"] = data["attachment_path"]
            if "claim_date" in data:
                update_data["claim_date"] = datetime.fromisoformat(data["claim_date"]) if data["claim_date"] else None
            if "claimer" in data:
                update_data["claimer"] = data["claimer"]
            if "safekeeper" in data:
                safekeepers = data["safekeeper"]
                if not isinstance(safekeepers, list):
                    return ServerResponse(message='Lista de safekeepers inválida', message_code=INVALID_SAFEKEEPER_LIST, status=StatusCode.BAD_REQUEST)
                validated_safekeepers = []
                for sk in safekeepers:
                    email = sk.get("user_email")
                    if not email or not re.match(r"^[\w\.-]+@utn\.ac\.cr$", email):
                        return ServerResponse(message=f'Dominio de correo electrónico inválido para safekeeper: {email}', message_code=INVALID_EMAIL_DOMAIN, status=StatusCode.BAD_REQUEST)
                    validated_safekeepers.append({"accepted": False, "user_email": email})
                update_data["safekeeper"] = validated_safekeepers
            if "user_email" in data:
                user_email = data["user_email"]
                if not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr)$", user_email):
                    return ServerResponse(message='Dominio de correo electrónico inválido', message_code=INVALID_EMAIL_DOMAIN, status=StatusCode.BAD_REQUEST)
                update_data["user_email"] = user_email

            if not update_data:
                return ServerResponse(message='No hay campos válidos para actualizar', message_code=NO_FIELDS_TO_UPDATE, status=StatusCode.BAD_REQUEST)

            update_result = LostObjectModel.update(object_id, update_data)

            if update_result.matched_count == 0:
                return ServerResponse(message='Objeto perdido no encontrado', message_code=NOT_FOUND, status=StatusCode.NOT_FOUND)

            return ServerResponse(data=update_data, message='Objeto perdido actualizado con éxito', status=StatusCode.OK)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

