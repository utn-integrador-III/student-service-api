from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
#efefr

class LostObjectsController(Resource):
    route = '/lost_objects'

    """
    Get lost_objects
    """
    def get(self):
        try:
            # Check connection status
            LostObjectModel.contextDB()
            return ServerResponse(message='Connection to DB is OK',
                                        message_code=HEALTH_SUCCESSFULLY, status=StatusCode.OK)         
        except Exception as ex:
            print(ex)
            logging.exception(ex)
            return ServerResponse(message='Connection to DB is not possible.',
                                      message_code=HEALTH_NOT_FOUND, status=StatusCode.NOT_FOUND)