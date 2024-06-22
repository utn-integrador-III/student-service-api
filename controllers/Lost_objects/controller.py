from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime
from bson import ObjectId  # Importar ObjectId para comprobación de tipo

class LostObjectsController(Resource):
    route = '/lostObjects'

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
