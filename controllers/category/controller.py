from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.category.model import CategoryModel
from controllers.category.parser import query_parser_save
import logging


class CategoryController(Resource):
    route = "/category"

    # Get all categories
    def get(self):
        try:
            categories = CategoryModel.getAll()
            if isinstance(categories, dict) and "error" in categories:
                return ServerResponse(
                    data={},
                    message=categories["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not categories:
                return ServerResponse(
                    data={},
                    message="No categories found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )

            for cat in categories:
                cat["_id"] = str(cat["_id"])
            return ServerResponse(data=categories, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    # Create a new category
    def post(self):
        try:
            data = request.get_json()
            if not data.get("category_name"):
                return ServerResponse(
                    message="Category name is required",
                    message_code=CATEGORY_NAME_REQUIRED,
                    status=StatusCode.BAD_REQUEST,
                )

            category_exists = CategoryModel.getByName(data.get("category_name"))
            if category_exists:
                return ServerResponse(
                    message="Category already exists",
                    message_code=CATEGORY_ALREADY_EXISTS,
                    status=StatusCode.CONFLICT,
                )

            category = CategoryModel.create(data)
            return ServerResponse(
                category.to_dict(),
                message="Category successfully created",
                message_code=CATEGORY_SUCCESFULLY_CREATED,
                status=StatusCode.CREATED,
            )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
