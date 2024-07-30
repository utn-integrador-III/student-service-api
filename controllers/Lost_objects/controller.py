from flask_restful import Resource
from flask import request
from models.category.model import CategoryModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from datetime import datetime
from bson import ObjectId
import pytz
import re
from .parser import LostObjectParser
from utils.auth_manager import auth_required

class LostObjectsController(Resource):
    route = '/lostObject'
    
    def get(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
        try:
            lost_objects = LostObjectModel.get_all()
            if isinstance(lost_objects, dict) and "error" in lost_objects:
                return ServerResponse(
                    data={},
                    message=lost_objects["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not lost_objects:  # If there are no lost objects
                return ServerResponse(
                    data={},
                    message="No lost objects found",
                    message_codes=NO_DATA,
                    status=StatusCode.OK,
                )

            def convert_object_id(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if isinstance(value, ObjectId):
                            obj[key] = str(value)
                        elif isinstance(value, datetime):
                            obj[key] = value.isoformat()
                        elif isinstance(value, list):
                            obj[key] = [convert_object_id(item) for item in value]
                        elif isinstance(value, dict):
                            obj[key] = convert_object_id(value)
                return obj

            lost_objects = [convert_object_id(obj) for obj in lost_objects]

            return ServerResponse(data=lost_objects, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    def post(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = {
                "name": (LOST_OBJECTS_NAME_REQUIRED, "Name is required"),
                "description": (LOST_OBJECTS_DESCRIPTION_REQUIRED, "Description is required"),
                "user_email": (LOST_OBJECTS_USER_EMAIL_REQUIRED, "User email is required"),
                "category": (LOST_OBJECTS_CATEGORY_REQUIRED, "Category is required"),
            }

            for field, (error_code, error_message) in required_fields.items():
                if not data.get(field):
                    return ServerResponse(
                        message=error_message,
                        message_code=error_code,
                        status=StatusCode.BAD_REQUEST,
                    )

            # Validate user email
            user_email = data["user_email"]
            if not re.match(r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr)$", user_email):
                return ServerResponse(
                    message="Invalid email domain",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.BAD_REQUEST,
                )

            # Validate and process safekeepers
            safekeepers = data.get("safekeeper", [])
            if not isinstance(safekeepers, list):
                return ServerResponse(
                    message="Safekeeper should be a list",
                    message_code=LOST_OBJECTS_SAFEKEEPER_REQUIRED,
                    status=StatusCode.BAD_REQUEST,
                )

            validated_safekeepers = []
            for sk in safekeepers:
                email = sk.get("user_email")
                if not email or not re.match(r"^[\w\.-]+@utn\.ac\.cr$", email):
                    return ServerResponse(
                        message=f"Invalid email domain for safekeeper: {email}",
                        message_code=INVALID_EMAIL_DOMAIN,
                        status=StatusCode.BAD_REQUEST,
                    )
                validated_safekeepers.append({"accepted": False, "user_email": email})

            # Validate and process categories
            category_names = data["category"]
            if not isinstance(category_names, list):
                category_names = [category_names]  # Convert to list if it's a single string

            categories = []
            for category_name in category_names:
                category = CategoryModel.find_by_name(category_name)
                if not category:
                    return ServerResponse(
                        message=f"Category not found: {category_name}",
                        message_code=CATEGORY_NOT_FOUND,
                        status=StatusCode.BAD_REQUEST,
                    )
                categories.append(category.to_dict())

            # Prepare data for creation
            creation_data = {
                "name": data["name"],
                "description": data["description"],
                "category": categories,
                "status": data.get("status", "Pending"),
                "creation_date": datetime.now(pytz.timezone("America/Costa_Rica")).replace(tzinfo=None),
                "attachment_path": data.get("attachment_path", "/lostObjects"),
                "claim_date": datetime.fromisoformat(data["claim_date"]) if data.get("claim_date") else None,
                "claimer": data.get("claimer", ""),
                "safekeeper": validated_safekeepers,
                "user_email": user_email,
            }

            # Create lost object
            lost_object = LostObjectModel.create(creation_data)

            return ServerResponse(
                data=lost_object.to_dict(),
                message="Lost object successfully created",
                message_code=LOST_OBJECTS_SUCCESSFULLY_CREATED,
                status=StatusCode.CREATED,
            )

        except Exception as ex:
            logging.exception(f"Unexpected error in post method: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    def put(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            logging.info(f"Current user: {current_user}")
        else:
            logging.warning("No user data available")

        try:
            args = LostObjectParser.parse_put_request()
            object_id = args.get('_id')

            if not ObjectId.is_valid(object_id):
                return ServerResponse(
                    message='Invalid or missing ID format',
                    message_code='INVALID_ID',
                    status=StatusCode.BAD_REQUEST
                )

            existing_document = LostObjectModel.getById(object_id)

            if not existing_document:
                return ServerResponse(
                    message='Lost object not found',
                    message_code='NOT_FOUND_MSG',
                    status=StatusCode.NOT_FOUND
                )

            update_data = {}
            simple_fields = ['name', 'description', 'status', 'attachment_path', 'user_email', 'claimer']
            for field in simple_fields:
                if args.get(field):
                    update_data[field] = args[field]

            if args.get("claim_date"):
                update_data["claim_date"] = datetime.fromisoformat(args["claim_date"]) if args["claim_date"] else None

            if args.get("safekeeper"):
                validated_safekeepers = []
                for sk in args["safekeeper"]:
                    email = sk.get("user_email")
                    if not email or not re.match(r"^[\w\.-]+@utn\.ac\.cr$", email):
                        return ServerResponse(
                            message=f"Invalid email domain for safekeeper: {email}",
                            message_code='INVALID_EMAIL_DOMAIN',
                            status=StatusCode.BAD_REQUEST
                        )
                    validated_safekeepers.append({"accepted": False, "user_email": email})
                update_data["safekeeper"] = validated_safekeepers

            if args.get("category"):
                category_names = args["category"]
                if not isinstance(category_names, list):
                    return ServerResponse(
                        message="Category should be a list",
                        message_code='LOST_OBJECTS_CATEGORY_REQUIRED',
                        status=StatusCode.BAD_REQUEST
                    )
                categories = []
                for category in category_names:
                    if not isinstance(category, str):
                        return ServerResponse(
                            message=f"Invalid category format: {category}",
                            message_code='INVALID_CATEGORY_FORMAT',
                            status=StatusCode.BAD_REQUEST
                        )
                    category_name = category.strip().lower()
                    category_doc = CategoryModel.find_by_name(category_name)
                    if not category_doc:
                        return ServerResponse(
                            message=f"Category '{category_name}' not found",
                            message_code='CATEGORY_NOT_FOUND',
                            status=StatusCode.BAD_REQUEST
                        )
                    categories.append(category_doc.to_dict())
                update_data["category"] = categories
            else:
                update_data["category"] = []

            existing_category_names = {cat.get('category_name', '').strip().lower() for cat in existing_document.get('category', [])}
            new_category_names = {cat.get('category_name', '').strip().lower() for cat in update_data.get('category', [])}

            if existing_category_names != new_category_names:
                update_result = LostObjectModel.update(object_id, update_data)

                if update_result.matched_count == 0:
                    return ServerResponse(
                        message='Lost object not found',
                        message_code='NOT_FOUND_MSG',
                        status=StatusCode.NOT_FOUND
                    )

                for field in ['creation_date', 'claim_date']:
                    if isinstance(update_data.get(field), datetime):
                        update_data[field] = update_data[field].isoformat()

                return ServerResponse(
                    data=update_data,
                    message='Lost object successfully updated',
                    message_code='LOST_OBJECTS_SUCCESSFULLY_UPDATED',
                    status=StatusCode.OK
                )
            else:
                return ServerResponse(
                    message='No changes detected in the category field',
                    message_code='NO_CHANGES',
                    status=StatusCode.OK
                )

        except Exception as ex:
            logging.exception(f"Unexpected error in put method: {ex}")
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)