from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.zone.model import ZoneModel
from controllers.zone.parser import query_parser_save
import logging


class ZoneController(Resource):
    route = "/zone"

    """
    Get all zones
    """

    def get(self):
        try:
            zones = ZoneModel.get_all()

            if isinstance(zones, dict) and "error" in zones:
                return ServerResponse(
                    data={},
                    message=zones["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not zones:  # If there are no zones
                return ServerResponse(
                    data=None,
                    message="Zones not found",
                    message_code=NO_DATA,
                    status=StatusCode.BAD_REQUEST,
                )


            # Convert ObjectId to string
            for zone in zones:
                zone["_id"] = str(zone["_id"])

            return ServerResponse(data=zones, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new zone 
    """
    def post(self):
        try:
            # Get data from the body of the request
            data = request.get_json()

            # Validate required name fields
            if not data.get("name"):
                return ServerResponse(message='Name is required', 
                                      message_code=ZONE_NAME_REQUIRED, status=StatusCode.BAD_REQUEST)
            
            # Validate required localization fields
            if not data.get("location"):
                return ServerResponse(message='Location is required', 
                                      message_code=ZONE_LOCATION_REQUIRED, status=StatusCode.BAD_REQUEST)

            # Validate if the zone already exists by name
            zone_exists = ZoneModel.get_by_name(data.get("name"))

            if zone_exists:
                return ServerResponse(message='Zone already exists', 
                                      message_code=ZONE_ALREADY_EXIST, status=StatusCode.CONFLICT)

            # Create and save the new zone
            zone = ZoneModel.create(data)
            return ServerResponse(zone.to_dict(), message="Zone successfully created", 
                                  message_code=ZONE_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


    def put(self):
        try:
            # Get update data from the request body
            update_data = request.get_json()

            # Validate if valid update data was provided
            if not update_data or not isinstance(update_data, dict) or len(update_data) == 0:
                return ServerResponse(
                    message="No valid data provided for update",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Extract ID from update data and ensure it's present
            id = update_data.get("_id")
            if not id:
                return ServerResponse(
                    message="ID is required in the update data",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Remove ID from update data to prevent updating the ID
            update_data.pop("_id", None)

            # Validate additional fields not allowed
            allowed_fields = {"name", "location"}  # Definir los campos permitidos
            additional_fields = set(update_data.keys()) - allowed_fields
            if additional_fields:
                return ServerResponse(
                    message=f"Additional fields not allowed: {', '.join(additional_fields)}",
                    message_code=INCORRECT_REQUEST_PARAM,
                    status=StatusCode.BAD_REQUEST,
                )

            # Check if the zone exists by ID
            zone = ZoneModel.get_by_id(id)
            if not zone:
                return ServerResponse(
                    message="Zone does not exist",
                    message_code=ZONE_NOT_FOUND,
                    status=StatusCode.BAD_REQUEST
                )

            # Update zone
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
    