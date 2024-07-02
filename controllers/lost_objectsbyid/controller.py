from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from controllers.Lost_objects.parser import query_parser_save
from flask_restful import Resource
from datetime import datetime
from bson import ObjectId
import pytz
from .parser import LostObjectParser

class LostObjectByIdController(Resource):
    routeById = "/lostObject/<string:id>"

    # Get a lost object by id
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


class LostObjectsDetailController(Resource):
    route = '/lostObject'

    def put(self):
        try:
            args = LostObjectParser.parse_put_request()
            object_id = args['_id']

            if not ObjectId.is_valid(object_id):
                return ServerResponse(message='Formato de ID inválido o ID faltante', message_code=INVALID_ID, status=StatusCode.BAD_REQUEST)

            update_data = {}
            if args.get("name"):
                update_data["name"] = args["name"]
            if args.get("description"):
                update_data["description"] = args["description"]
            if args.get("status"):
                update_data["status"] = args["status"]
            if args.get("attachment_path"):
                update_data["attachment_path"] = args["attachment_path"]
            if args.get("claim_date"):
                update_data["claim_date"] = datetime.fromisoformat(args["claim_date"]) if args["claim_date"] else None
            if args.get("claimer"):
                update_data["claimer"] = args["claimer"]
            if args.get("safekeeper"):
                validated_safekeepers = []
                for sk in args["safekeeper"]:
                    validated_safekeepers.append({"accepted": False, "user_email": sk["user_email"]})
                update_data["safekeeper"] = validated_safekeepers
            if args.get("user_email"):
                update_data["user_email"] = args["user_email"]

            if not update_data:
                return ServerResponse(message='No hay campos válidos para actualizar', message_code=NO_FIELDS_TO_UPDATE, status=StatusCode.BAD_REQUEST)

            update_result = LostObjectModel.update(object_id, update_data)

            if update_result.matched_count == 0:
                return ServerResponse(message='Objeto perdido no encontrado', message_code=NOT_FOUND, status=StatusCode.NOT_FOUND)

            return ServerResponse(data=update_data, message='Objeto perdido actualizado con éxito', status=StatusCode.OK)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
