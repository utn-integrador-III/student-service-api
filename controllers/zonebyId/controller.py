from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode, OK_MSG, NO_DATA, INVALID_ID, ZONE_SUCCESSFULLY_DELETED
from models.zone.model import ZoneModel
import logging
from bson.errors import InvalidId


class ZoneByIdController(Resource):

    route = "/zone/<string:id>"

    def get(self, id):
        """
        Get a zone by ID
        """
        try:
            result = ZoneModel.get_by_id(id)
            if result:
                # Convert ObjectId to string
                result['_id'] = str(result['_id']) if '_id' in result else None
                return ServerResponse(
                    data=result, 
                    message="Zone found", 
                    message_code=OK_MSG, 
                    status=StatusCode.OK
                )
            else:
                return ServerResponse(
                    data={}, 
                    message="Zone does not exist", 
                    message_code=NO_DATA, 
                    status=StatusCode.OK
                )
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data={},
                message="Invalid zone ID",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )
        except Exception as ex:
            logging.error(f"Error getting zone by ID: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    def delete(self, id):
        """
        Delete a zone by ID
        """
        try:
            result = ZoneModel.delete(id)
            if result:
                return ServerResponse(
                    message="Zone successfully deleted",
                    message_code=ZONE_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The zone does not exist and cannot be deleted.",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(f"Error deleting zone by ID: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
