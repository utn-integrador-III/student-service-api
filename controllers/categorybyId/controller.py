from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.category.model import CategoryModel
from controllers.category.parser import query_parser_save
import logging


class CategoryByIdController(Resource):
    routeById = "/category/<string:id>"

    # Get a category by id
    def get(self, id):
        try:
            result = CategoryModel.getById(id)
            if result:
                result["_id"] = str(result["_id"]) if "_id" in result else None
                return ServerResponse(
                    data=result,
                    message="Category found",
                    message_code=OK_MSG,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Category does not exist",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.error(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    # Update an existing category by id
    def put(self, id):
        try:
            data = request.get_json()
            updated_count = CategoryModel.update(id, data)

            if updated_count is None:
                return ServerResponse(
                    data={},
                    message="Category successfully updated",
                    message_code=CATEGORY_SUCCESFULLY_UPDATED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="Category not found or category already exists",
                    message_code=NO_DATA,
                    status=StatusCode.NOT_FOUND,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(
                data={},
                message="Category not found or category already exists.",
                message_code=NO_DATA,
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )

    # Delete a category by id
    def delete(self, id):
        try:
            if CategoryModel.delete(id):
                return ServerResponse(
                    message="Category successfully deleted",
                    message_code=CATEGORY_SUCCESFULLY_DELETED,
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    data={},
                    message="The category does not exist and cannot be deleted.",
                    message_code=NO_DATA,
                    status=StatusCode.OK,
                )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
