from flask_restful import Resource

from utils.server_response import *
from models.zone.model import ZoneModel
from controllers.zone.parser import query_parser_save
import logging


class ZoneByIdController(Resource):
    route = "/zone/<string:id>"

    """
    Get all sites
    """

    def get(self):
        try:
            zone = ZoneModel.get_by_id()

            data = [c.to_dict() for c in zone]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete a zone by ID
    """

    def delete(self, id):
        try:
            result = ZoneModel.delete(id)
            if result:
                return ServerResponse(
                    message="Zone successfully deleted",
                    message_code=ZONE_SUCCESSFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The zone no exists and cannot be deleted.",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
