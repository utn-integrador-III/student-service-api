from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_object import LostObject
import logging

class LostObjectsController(Resource):
    route = '/lost_objects'

    """
    Get all lost objects
    """
    def get(self):
        try:
            # Retrieve all lost objects from the database
            lost_objects = LostObject.query.all()
            if lost_objects:
                return ServerResponse(message='Lost objects retrieved successfully',
                                      data=[obj.json() for obj in lost_objects],
                                      message_code=SUCCESS, status=StatusCode.OK)
            else:
                return ServerResponse(message='No lost objects found',
                                      message_code=NOT_FOUND, status=StatusCode.NOT_FOUND)
        except Exception as ex:
            print(ex)
            logging.exception(ex)
            return ServerResponse(message='Failed to retrieve lost objects',
                                  message_code=SERVER_ERROR, status=StatusCode.INTERNAL_SERVER_ERROR)
