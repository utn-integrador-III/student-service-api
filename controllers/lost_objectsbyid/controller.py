from flask_restful import Resource
from utils.server_response import *
from models.lost_objects.model import LostObjectModel
import logging
from bson.errors import InvalidId


class LostObjectByIdController(Resource):

    routeById = "/lostObject/<string:id>"

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
        
   
    