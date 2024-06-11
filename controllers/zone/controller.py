from flask_restful import Resource

from utils.server_response import *
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

            if not zones:  # If there are no zones
                return ServerResponse(data={}, message="No zones", message_code="NO_DATA", status=StatusCode.OK)

            data = [c.to_dict() for c in zones]
            return ServerResponse(data, status=StatusCode.OK)
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


  
