from flask_restful import Resource
from flask import Request, request
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
from werkzeug.exceptions import BadRequest


class LostObjectsController(Resource):
    route = "/lostObject"

    def get(self, **kwargs):
        current_user = kwargs.get("current_user", None)
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
                    message_code=INTERNAL_SERVER_ERROR_MSG,
                )

            if not lost_objects:  # If there are no lost objects
                return ServerResponse(
                    data=None,
                    message=LOST_OBJECTS_NOT_FOUND,
                    message_code=NO_DATA,
                    status=StatusCode.NOT_FOUND,
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

            return ServerResponse(
                data=lost_objects,
                status=StatusCode.OK,
                message_code=OK_MSG,
                message=LOST_OBJECTS_FOUND,
            )
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    @auth_required(permission="write")
    def post(self, **kwargs):
        current_user = kwargs.get("current_user")
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")

        try:
            data = request.get_json()

            # Validate required fields
            required_fields = {
                "name": (LOST_OBJECTS_NAME_REQUIRED, "Name is required"),
                "description": (
                    LOST_OBJECTS_DESCRIPTION_REQUIRED,
                    "Description is required",
                ),
                "user_email": (
                    LOST_OBJECTS_USER_EMAIL_REQUIRED,
                    "User email is required",
                ),
                "category": (LOST_OBJECTS_CATEGORY_REQUIRED, "Category is required"),
                # "safekeeper": (LOST_OBJECTS_SAFEKEEPER_REQUIRED, "Safekeeper is required"),
                # "attachment_path": (INCORRECT_REQUEST_PARAM, "Attachment path is required")
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
            if not re.match(
                r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr|adm\.utn\.ac\.cr)$",
                user_email,
            ):
                return ServerResponse(
                    message="Invalid email domain",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.BAD_REQUEST,
                )

            # Validate and process safekeepers
            safekeepers = data.get("safekeeper", [])
            if not isinstance(safekeepers, list):
                safekeepers = [safekeepers]  # Convert to list if it's a single item

            validated_safekeepers = []
            for sk in safekeepers:
                email = sk.get("user_email") if isinstance(sk, dict) else sk
                if not email or not re.match(
                    r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr|adm\.utn\.ac\.cr)$", email
                ):
                    return ServerResponse(
                        message=f"Invalid email domain for safekeeper: {email}",
                        message_code=INVALID_EMAIL_DOMAIN,
                        status=StatusCode.BAD_REQUEST,
                    )
                validated_safekeepers.append({"accepted": False, "user_email": email})

            # Validate and process categories
            category_names = data["category"]
            if not isinstance(category_names, list):
                category_names = [
                    category_names
                ]  # Convert to list if it's a single string

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
                "status": "Pending",
                "creation_date": datetime.now(
                    pytz.timezone("America/Costa_Rica")
                ).replace(tzinfo=None),
                "attachment_path": data.get("attachment_path", "/lostObjects"),
                "claim_date": None,
                "claimer": None,
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

    @auth_required(permission="update")
    def put(self, **kwargs):
        current_user = kwargs.get("current_user", None)
        if current_user:
            logging.info(f"Current user: {current_user}")
        else:
            logging.warning("No user data available")

        try:
            args = LostObjectParser.parse_put_request()
            object_id = args.get("_id")

            if not ObjectId.is_valid(object_id):
                return ServerResponse(
                    message="Invalid or missing ID format",
                    message_code="INVALID_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                )

            existing_document = LostObjectModel.getById(object_id)

            if not existing_document:
                return ServerResponse(
                    message="Lost object not found",
                    message_code="NOT_FOUND_MSG",
                    status=StatusCode.NOT_FOUND,
                )

            update_data = {}
            simple_fields = [
                "name",
                "description",
                "status",
                "attachment_path",
                "user_email",
                "claim_date",
                "claimer",
            ]
            for field in simple_fields:
                if args.get(field) and args.get(field) != existing_document.get(field):
                    update_data[field] = args[field]

            if args.get("claim_date"):
                claim_date = (
                    datetime.fromisoformat(args["claim_date"])
                    if args["claim_date"]
                    else None
                )
                if claim_date != existing_document.get("claim_date"):
                    update_data["claim_date"] = claim_date

            # Validate and process safekeeper
            if args.get("safekeeper") and args.get(
                "safekeeper"
            ) != existing_document.get("safekeeper"):
                update_data["safekeeper"] = args["safekeeper"]

            # Validate and process categories
            if args.get("category"):
                category_names = args["category"]
                if not isinstance(category_names, list):
                    category_names = [
                        category_names
                    ]  # Convert to list if it's a single string

                categories = []
                for category_name in category_names:
                    category = CategoryModel.find_by_name(category_name)
                    if not category:
                        return ServerResponse(
                            message=f"Category not found: {category_name}",
                            message_code="CATEGORY_NOT_FOUND",
                            status=StatusCode.NOT_FOUND,
                        )
                    categories.append(
                        category.to_dict()
                    )  # Store the complete category object

                if categories != existing_document.get("category"):
                    update_data["category"] = categories

            if update_data:
                update_result = LostObjectModel.update(object_id, update_data)

                if update_result.matched_count == 0:
                    return ServerResponse(
                        message="Lost object not found",
                        message_code="NOT_FOUND_MSG",
                        status=StatusCode.NOT_FOUND,
                    )

                for field in ["creation_date", "claim_date"]:
                    if isinstance(update_data.get(field), datetime):
                        update_data[field] = update_data[field].isoformat()

                return ServerResponse(
                    data=update_data,
                    message="Lost object successfully updated",
                    message_code="LOST_OBJECTS_SUCCESSFULLY_UPDATED",
                    status=StatusCode.OK,
                )
            else:
                return ServerResponse(
                    message="No changes detected",
                    message_code="NO_CHANGES",
                    status=StatusCode.BAD_REQUEST,
                )

        except BadRequest as ex:
            return ServerResponse(
                message=ex.description,
                message_code="BAD_REQUEST",
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.exception(f"Unexpected error in put method: {ex}")
            return ServerResponse(
                message="An unexpected error occurred",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )

    @auth_required(permission="update")
    def patch(self, **kwargs):
        current_user = kwargs.get("current_user", None)
        if current_user:
            logging.info(f"Current user: {current_user}")
        else:
            logging.warning("No user data available")

        try:
            data = request.get_json()
            logging.info(f"Received data: {data}")

            object_id = data.get("_id")
            if not object_id:
                logging.error("Missing '_id' in request data")
                return ServerResponse(
                    message="Invalid or missing ID format",
                    message_code="INVALID_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                )

            if not ObjectId.is_valid(object_id):
                logging.error("Invalid ObjectId format")
                return ServerResponse(
                    message="Invalid or missing ID format",
                    message_code="INVALID_ID",
                    status=StatusCode.UNPROCESSABLE_ENTITY,
                )

            existing_document = LostObjectModel.getById(object_id)
            if not existing_document:
                logging.error("Lost object not found")
                return ServerResponse(
                    message="Lost object not found",
                    message_code="NOT_FOUND_MSG",
                    status=StatusCode.NOT_FOUND,
                )

            update_data = {}
            status = data.get("status")
            if status not in ["Claimed", "Cancelled"]:
                logging.error(f"Invalid status: {status}")
                return ServerResponse(
                    message="Invalid status. Must be 'Claimed' or 'Cancelled'",
                    message_code="INVALID_STATUS",
                    status=StatusCode.BAD_REQUEST,
                )

            update_data["status"] = status

            if status == "Cancelled":
                logging.info("Processing Cancelled status")
                update_data["claimer"] = ""
                update_data["claim_date"] = None
            elif status == "Claimed":
                logging.info("Processing Claimed status")
                email_claimer = data.get(
                    "email_claimer"
                )  # Cambiado de "claimer" a "email_claimer"
                if not email_claimer:
                    logging.error("Missing claimer email")
                    return ServerResponse(
                        message="Email for claimer is required",
                        message_code="EMAIL_REQUIRED",
                        status=StatusCode.BAD_REQUEST,
                    )
                if not re.match(
                    r"^[\w\.-]+@(utn\.ac\.cr|est\.utn\.ac\.cr|adm\.utn\.ac\.cr)$",
                    email_claimer,
                ):
                    logging.error(f"Invalid email for claimer: {email_claimer}")
                    return ServerResponse(
                        message="Invalid email for claimer",
                        message_code="INVALID_EMAIL",
                        status=StatusCode.BAD_REQUEST,
                    )
                update_data["claimer"] = email_claimer
                update_data["claim_date"] = datetime.now(
                    pytz.timezone("America/Costa_Rica")
                ).replace(tzinfo=None)

            safekeeper_email = data.get(
                "safekeeper_email"
            )  # Cambiado de "safekeeper" a "safekeeper_email"
            logging.info(f"Processing safekeeper email: {safekeeper_email}")
            if safekeeper_email and isinstance(
                existing_document.get("safekeeper"), list
            ):
                update_data["safekeeper"] = [
                    (
                        {**sk, "accepted": True}
                        if sk["user_email"] == safekeeper_email
                        else sk
                    )
                    for sk in existing_document["safekeeper"]
                ]

            if update_data:
                logging.info(f"Updating data: {update_data}")
                update_result = LostObjectModel.update(object_id, update_data)

                if update_result.matched_count == 0:
                    logging.error("Lost object not found during update")
                    return ServerResponse(
                        message="Lost object not found",
                        message_code="NOT_FOUND_MSG",
                        status=StatusCode.NOT_FOUND,
                    )

                for field in ["creation_date", "claim_date"]:
                    if isinstance(update_data.get(field), datetime):
                        update_data[field] = update_data[field].isoformat()

                return ServerResponse(
                    data=update_data,
                    message="Lost object successfully updated",
                    message_code="LOST_OBJECTS_SUCCESSFULLY_UPDATED",
                    status=StatusCode.OK,
                )
            else:
                logging.warning("No changes detected in the update request")
                return ServerResponse(
                    message="No changes detected",
                    message_code="NO_CHANGES",
                    status=StatusCode.BAD_REQUEST,
                )

        except BadRequest as ex:
            logging.error(f"BadRequest error: {ex}")
            return ServerResponse(
                message=ex.description,
                message_code="BAD_REQUEST",
                status=StatusCode.BAD_REQUEST,
            )

        except Exception as ex:
            logging.exception(f"Unexpected error in patch method: {ex}")
            return ServerResponse(
                message="An unexpected error occurred",
                message_code="INTERNAL_SERVER_ERROR",
                status=StatusCode.INTERNAL_SERVER_ERROR,
            )
