from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from models.safekeeper.model import SafekeeperModel
import logging

class SafekeeperController(Resource):
    route = "/safekeeper"

    def get(self, **kwargs):
        try:
            safekeepers = SafekeeperModel.getAll()
            if isinstance(safekeepers, dict) and "error" in safekeepers:
                return ServerResponse(
                    data={},
                    message=safekeepers["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not safekeepers:
                return ServerResponse(
                    data={},
                    message="No safekeepers found",
                    status=StatusCode.NOT_FOUND,
                )

            for safekeeper in safekeepers:
                safekeeper["_id"] = str(safekeeper["_id"])
            return ServerResponse(data=safekeepers, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)