from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime
from controllers.Lost_objects.parser import query_parser_save
import logging
import pytz

class LostObjectsController(Resource):
    route = '/lostObject'

    """
    Get all lost objects
    """
    def get(self):
        try:
            lost_objects = LostObjectModel.get_all()

            if isinstance(lost_objects, dict) and "error" in lost_objects:
                return ServerResponse(data={}, message=lost_objects["error"], status=StatusCode.INTERNAL_SERVER_ERROR)

            if not lost_objects:  # If there are no lost objects
                return ServerResponse(data={}, message="No lost objects found", message_codes=NO_DATA, status=StatusCode.OK)

            # Convert ObjectId to string and datetime to ISO format string
            for obj in lost_objects:
                obj['_id'] = str(obj['_id'])
                obj['creation_date'] = obj['creation_date'].isoformat() if obj.get('creation_date') else None
                obj['claim_date'] = obj['claim_date'].isoformat() if obj.get('claim_date') else None

            return ServerResponse(data=lost_objects, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


    def post(self):
        try:
            # Get data from the request body
            data = request.get_json()

            # Validate required name fields
            if not data.get("name"):
                return ServerResponse(message='Name is required', 
                                      message_code=LOST_OBJECTS_NAME_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate required description fields
            if not data.get("description"):
                return ServerResponse(message='Description is required', 
                                      message_code=LOST_OBJECTS_DESCRIPTION_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate if the lost object already exists by name
            object_exists = LostObjectModel.get_by_name(data.get("name"))
            if object_exists:
                return ServerResponse(message='Lost_object already exists', 
                                      message_code=LOST_OBJECTS_EXIST, status=StatusCode.CONFLICT)

            # Set the status to "Pending"
            data["status"] = "Pending"

            # Set the attachment path to "/lost Objects"
            data["attachment_path"] = '/lostObjects'

            # Set the creation date to Costa Rica time
            data["creation_date"] = datetime.now(pytz.timezone('America/Costa_Rica')).replace(tzinfo=None)

            # Set claim_date to None
            data["claim_date"] = None

            # Create and save the new lost object
            lost_object = LostObjectModel.create(data)
            return ServerResponse(lost_object.to_dict(), message="Lost_object successfully created", 
                                  message_code=LOST_OBJECTS_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)