from flask_restful import Resource

from utils.server_response import *
from models.site.model import SiteModel
from controllers.site.parser import query_parser_save
import logging


class SiteController(Resource):
    route = '/booking_api/site'

    """
    Get all sites
    """
    def get(self):        
        try:
            sites = SiteModel.get_all()

            data = [c.to_dict() for c in sites]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new site 
    """
    def post(self):
        data = query_parser_save().parse_args()
        try:
            # Validate unique name
            site_exists = SiteModel.get_by_name(data["name"], data["country_id"])
            if site_exists:
                return ServerResponse(message='Site aready exist', 
                                      message_code=SITE_ALREADY_EXIST, status=StatusCode.CONFLICT)
            site = SiteModel(**data)
            site.insert()
            site = SiteModel.get_by_id(site._id)
            return ServerResponse(site.to_dict(), message="Site successfully created", 
                                  message_code=SITE_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


  
