from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from bson import ObjectId

class LostObjectByIdController(Resource):
    routeById = "/lostObject/<string:id>"

    def get(self, id):
        try:
            result = LostObjectModel.getById(id)
            if result:
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message=LOST_OBJECTS_FOUND,
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message=LOST_OBJECTS_NOT_FOUND,
                    message_code=NO_DATA,
                    status=StatusCode.BAD_REQUEST,
                )
        except Exception as ex:
            logging.error(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    def delete(self, id):
        try:
            result = LostObjectModel.delete(id)
            if result:
                return ServerResponse(
                    message="Report successfully deleted",
                    message_code=LOST_OBJECT_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The report do not exist and cannot be deleted.",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
