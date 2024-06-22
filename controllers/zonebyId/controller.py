from bson import ObjectId
from flask_restful import Resource
from utils.server_response import *
from models.zone.model import ZoneModel
import logging
from bson.errors import InvalidId


class ZoneByIdController(Resource):

    route = "/zone/<string:id>"

    """
    Get all sites
    """
    
    def get(self, id):
        try:
            result = ZoneModel.get_by_id(id)
            if result:
                # Change to string the ObjectId
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message="Successfully requested",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data=None,
                    message="Zone not found",
                    message_code=NO_DATA,
                    status=StatusCode.BAD_REQUEST,
                )

        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data=None,
                message="Invalid Id",
                message_code=INVALID_ID,
                status=StatusCode.UNPROCESSABLE_ENTITY,
            )

        except Exception as ex:
            logging.error(f"Error getting zone by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete a zone by ID
    """


    def delete(self, id):
        try:
            # Validate if the id is a valid ObjectId
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")

            result = ZoneModel.delete(id)
            if result:
                return ServerResponse(
                    message="Zone successfully deleted",
                    message_code=ZONE_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data=None,
                    message="Zone not found",
                    message_code=ZONE_ITEM_NOT_FOUND,  # Changed from message_codes to message_code
                    status=StatusCode.OK,
                )
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            return ServerResponse(
                data=None,
                message="Invalid Id",
                message_code=INVALID_ID,
                status=StatusCode.UNPROCESSABLE_ENTITY,
            )
        except Exception as ex:
            logging.exception(f"Error deleting zone by id: {ex}")
            return ServerResponse(
                data=None,
                message="An error occurred while trying to delete the zone.",
                message_code=ERROR_DELETE,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )
        
   
    