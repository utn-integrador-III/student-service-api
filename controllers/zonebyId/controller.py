from flask_restful import Resource
from utils.server_response import *
from models.zone.model import ZoneModel
from controllers.zone.parser import query_parser_save
import logging


class ZoneByIdController(Resource):
    route = "/zone/<id>"

    def get(self, id):
        try:
            result = ZoneModel.get_by_id(id)
            if result:
                # change to string the ObjectId
                result['_id'] = str(result['_id']) if '_id' in result else None
                return ServerResponse(data=result, message="Zone found", message_code=OK_MSG, status=StatusCode.OK)
            else:
                return ServerResponse(data={}, message="Zone not found", message_code=NO_DATA, status=StatusCode.NOT_FOUND)
        
        except Exception as ex:
            logging.error(f"Error getting zone by id: {ex}")
            return ServerResponse(message="Internal server error", message_code=INTERNAL_SERVER_ERROR_MSG, status=StatusCode.INTERNAL_SERVER_ERROR)
