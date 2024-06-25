from flask_restful import Resource
from utils.server_response import *
from models.lost_objects.model import LostObjectModel
import logging
from bson.errors import InvalidId


class LostObjectByIdController(Resource):

    route = "/lostObject/<string:id>"
    
    """
    Get lostObject Report
    """
    
    def get(self,id):
        try:
            result = LostObjectModel.get_by_id(id)
            if result:
                # Change to string the ObjectId
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message="Report found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Report does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
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
            logging.error(f"Error getting zone by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
    """
    Delete a lostObject Report by ID
    """

    def delete(self, id):
        try:
            result = LostObjectModel.delete(id)
            if result:
                return ServerResponse(
                    message="Report successfully deleted",
                    message_code=LOST_OBJECTS_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The report do not exist and cannot be deleted.",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
   
    