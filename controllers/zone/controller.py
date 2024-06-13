from flask_restful import Resource

from utils.server_response import *
from utils.message_codes import *
from models.zone.model import ZoneModel
from controllers.zone.parser import query_parser_save
import logging

class ZoneController(Resource):
    route = '/zone'

    """
    Get all zones
    """

    def get(self):
        try:
            zones = ZoneModel.get_all()

            if isinstance(zones, dict) and "error" in zones:
                return ServerResponse(data={}, message=zones["error"], status=StatusCode.INTERNAL_SERVER_ERROR)

            if not zones:  # If there are no zones
                return ServerResponse(data={}, message="No zones found", message_codes=NO_DATA, status=StatusCode.OK)

            # Convert ObjectId to string
            for zone in zones:
                zone['_id'] = str(zone['_id'])

            return ServerResponse(data=zones, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


    """
    Create a new zone 
    """
    # def post(self):
    #     data = query_parser_save().parse_args()
    #     try:
    #         # Validate unique name
    #         site_exists = SiteModel.get_by_name(data["name"], data["country_id"])
    #         if site_exists:
    #             return ServerResponse(message='Site aready exist', 
    #                                   message_code=SITE_ALREADY_EXIST, status=StatusCode.CONFLICT)
    #         site = SiteModel(**data)
    #         site.insert()
    #         site = SiteModel.get_by_id(site._id)
    #         return ServerResponse(site.to_dict(), message="Site successfully created", 
    #                               message_code=SITE_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
    #     except Exception as ex:
    #         logging.exception(ex)
    #         return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


  
