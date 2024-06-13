# controllers/lost_objects/controller.py
from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime

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

            # Convert ObjectId to string and datetime to ISO format string
            for obj in lost_objects:
                obj['_id'] = str(obj['_id'])
                obj['creation_date'] = obj['creation_date'].isoformat() if obj.get('creation_date') else None
                obj['claim_date'] = obj['claim_date'].isoformat() if obj.get('claim_date') else None

            return ServerResponse(data=lost_objects, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
