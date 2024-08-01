from functools import wraps
import requests
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from decouple import config
import logging

def auth_required(action=None, permission='', with_args=False):
    def decorator(f):
        @wraps(f)
        def catcher(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return ServerResponse(
                    data=None,
                    message="Authorization token is required",
                    message_code=AUTH_TOKEN_REQUIRED,
                    status=StatusCode.UNAUTHORIZED
                )

            try:
                body = {'permission': permission}
                response = requests.post(
                    f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/auth/verify_auth",
                    json=body,
                    headers={'Authorization': token},
                    timeout=20
                )
                response.raise_for_status()
                response_data = response.json()

                if "data" not in response_data:
                    return ServerResponse(
                        data=None,
                        message="No user data in authentication response",
                        message_code='USER_DATA_NOT_FOUND',
                        status=StatusCode.UNAUTHORIZED
                    )

                user_data = response_data["data"]
                email = user_data.get("email")
                name = user_data.get("rolName")

                if permission:
                    role_response = requests.get(
                        f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/rol",
                        json={'name': name}
                    )
                    role_response.raise_for_status()
                    role_permissions = role_response.json()["data"]["permissions"]
                    if permission not in role_permissions:
                        return ServerResponse(
                            data=None,
                            message="Permission denied",
                            message_code=PERMISSION_DENIED,
                            status=StatusCode.FORBIDDEN
                        )

                if with_args:
                    kwargs['current_user'] = {
                        'email': email,
                        'rolName': name
                    }

                return f(*args, **kwargs)
            except requests.RequestException as ex:
                logging.error(f"Error in authentication request: {str(ex)}")
                return ServerResponse(
                    data=None,
                    message=f"Error in authentication occurred: {str(ex)}",
                    message_code=AUTH_REQUEST_ERROR,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )
            except ValueError as ex:
                logging.error(f"Error processing authentication response: {str(ex)}")
                return ServerResponse(
                    data=None,
                    message=f"Error processing authentication response: {str(ex)}",
                    message_code=AUTH_PROCESSING_ERROR,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )
        return catcher
    return decorator
