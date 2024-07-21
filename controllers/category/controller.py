from bson import ObjectId
from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
from models.category.model import CategoryModel
from controllers.category.parser import query_parser_put, query_parser_save
import logging
from utils.auth_manager import auth_required


class CategoryController(Resource):
    route = "/category"

    # Get all categories
    @auth_required(permission="read", with_args=True)
    def get(self, **kwargs):
        current_user = kwargs.get("current_user", None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
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
                    status=StatusCode.BAD_REQUEST,
                )

            for cat in categories:
                cat["_id"] = str(cat["_id"])
            return ServerResponse(data=categories, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    # Create a new category
    @auth_required(permission="write", with_args=True)
    def post(self, **kwargs):
        current_user = kwargs.get("current_user", None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            data = request.get_json()
            category_name = data.get("category_name", "").strip()
            if not category_name:
                return ServerResponse(
                    data={},
                    message="Category name cannot be empty",
                    message_code=EMPTY_CATEGORY_NAME,
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

    # Update an existing category by id
    @auth_required(permission="update", with_args=True)
    def put(self, **kwargs):
        current_user = kwargs.get("current_user", None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")

        try:
            parser = query_parser_put()
            args = parser.parse_args()
            object_id = args["_id"]
            if not ObjectId.is_valid(object_id):
                return ServerResponse(
                    message="Invalid ID format or missing ID",
                    message_code=INVALID_ID,
                    status=StatusCode.BAD_REQUEST,
                )
            object_id = ObjectId(object_id)
            data = {"category_name": args["category_name"]}
            updated_count = CategoryModel.update(object_id, data)
            if updated_count:
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
