from flask import request
from flask_restful import Resource
from utils.server_response import *
from models.zone.model import ZoneModel
import logging


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
                    message="Zone found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Zone does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )

        except Exception as ex:
            logging.error(f"Error getting zone by id: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete a zone by ID
    """

    def delete(self, id):
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
                    message="The zone no exists and cannot be deleted.",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
   
    def put(self, id):
        try:
            # Get update data from the request body
            update_data = request.get_json()

           # Validate if valid update data was provided
            if not update_data or not isinstance(update_data, dict) or len(update_data) == 0:
                return ServerResponse(
                    message="No valid data provided for update",
                    message_code=NO_DATA,
                    status=StatusCode.BAD_REQUEST,
                )

           # Validate additional fields not allowed
            allowed_fields = {"name", "location"}  # Definir los campos permitidos
            additional_fields = set(update_data.keys()) - allowed_fields
            if additional_fields:
                return ServerResponse(
                    message=f"Additional fields not allowed: {', '.join(additional_fields)}",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST
                )
            # Check if the zone exists by ID
            zone = ZoneModel.get_by_id(id)
            if not zone:
                return ServerResponse(
                    message="Zone does not exist",
                    message_code=ZONE_NOT_FOUND,
                    status=StatusCode.OK,
                )

            #Update zone
            updated_zone = ZoneModel.update(id, update_data)
            if not updated_zone:
                return ServerResponse(
                    message="An error occurred while updating the zone",
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            # Convert ObjectId to string if it exists in the updated zone
            updated_zone["_id"] = str(updated_zone["_id"]) if "_id" in updated_zone else None

            # Successful response
            return ServerResponse(
                data=updated_zone,
                message="Zone successfully updated",
                message_code=ZONE_SUCCESSFULLY_UPDATED,
                status=StatusCode.OK,
            )

        except ValueError as ex:
            # Invalid ID handling
            logging.error(f"Invalid ID: {ex}")
            return ServerResponse(
                message="Invalid ID format",
                message_code=INVALID_ID,
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            # General exception handling
            logging.error(f"Unexpected error: {ex}")
            return ServerResponse(
                message="An error occurred while updating the zone",
                message_code=INTERNAL_SERVER_ERROR_MSG,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )