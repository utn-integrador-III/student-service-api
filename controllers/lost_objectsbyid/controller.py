from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.lost_objects.model import LostObjectModel
import logging
from bson import ObjectId
from utils.auth_manager import auth_required

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
    
    @auth_required(permission='delete', with_args=True)
    def delete(self, id, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")

        try:
            # Validate the ID format
            if not ObjectId.is_valid(id):
                return ServerResponse(
                    message='Invalid or missing ID format',
                    message_code='INVALID_ID',
                    status=StatusCode.UNPROCESSABLE_ENTITY
                )

            # Fetch the existing document
            existing_document = LostObjectModel.getById(id)
            if not existing_document:
                return ServerResponse(
                    data={},
                    message="The report does not exist and cannot be deleted.",
                    message_code='NO_DATA',
                    status=StatusCode.NOT_FOUND
                )

            if existing_document.get("user_email") != current_user.get("email"):
                return ServerResponse(
                    message=f'User email does not match.',
                    message_code='USER_EMAIL_MISMATCH',
                    status=StatusCode.FORBIDDEN
                )

            if existing_document.get("status") != 'Pending':
                return ServerResponse(
                    message=f'Cannot delete object because status is not Pending.',
                    message_code='STATUS_NOT_PENDING',
                    status=StatusCode.FORBIDDEN
                )

            # Proceed with deletion
            delete_result = LostObjectModel.delete(id)
            if delete_result.deleted_count == 0:
                return ServerResponse(
                    message='Failed to delete the document. No document was removed.',
                    message_code='INTERNAL_SERVER_ERROR',
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )

            return ServerResponse(
                message="Lost object successfully deleted",
                message_code='LOST_OBJECT_SUCCESSFULLY_DELETED',
                status=StatusCode.OK,
            )

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(
                message='An unexpected error occurred',
                message_code='INTERNAL_SERVER_ERROR',
                status=StatusCode.INTERNAL_SERVER_ERROR
            )
