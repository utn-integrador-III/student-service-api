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
                    data={},
                    message="No zones found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
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
