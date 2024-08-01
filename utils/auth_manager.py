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
                # Send Permission to verify if the user has authorization
                body = {'permission': permission}
                response = requests.post(
                    f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/auth/verify_auth",
                    json=body,
                    headers={'Authorization': token},
                    timeout=20
                )
                response.raise_for_status()
            except requests.RequestException as ex:
                logging.error(f"Error in authentication request: {str(ex)}")
                return ServerResponse(
                    data=None,
                    message=f"Error in authentication occurred: {str(ex)}",
                    message_code=AUTH_REQUEST_ERROR,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    name = response_data["data"]["rolName"]
                    
                    bodyRole = {'name': name}
                    # Make request to security API to check role permissions
                    role_response = requests.get(
                        f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/rol",
                        json=bodyRole,
                    )
                    role_response.raise_for_status()

                    role_response_data = role_response.json()
                    role_permissions = role_response_data["data"]["permissions"]
                    if permission in role_permissions:
                        if with_args:
                            kwargs['current_user'] = response_data["data"]
                        return f(*args, **kwargs)
                    else:
                        return ServerResponse(
                            data=None,
                            message="Permission denied",
                            message_code=PERMISSION_DENIED,
                            status=StatusCode.FORBIDDEN
                        )
                except (requests.RequestException, ValueError) as ex:
                    logging.error(f"Error processing authentication response: {str(ex)}")
                    return ServerResponse(
                        data=None,
                        message=f"Error processing authentication response: {str(ex)}",
                        message_code=AUTH_PROCESSING_ERROR,
                        status=StatusCode.INTERNAL_SERVER_ERROR
                    )
            else:
                try:
                    error_response = response.json()
                except ValueError:
                    logging.error(f"Error decoding JSON response: Response content: {response.content}")
                    return ServerResponse(
                        data=None,
                        message="Invalid response format from auth service",
                        message_code=INVALID_RESPONSE_FORMAT,
                        status=StatusCode.INTERNAL_SERVER_ERROR
                    )
                return ServerResponse(
                    data=error_response,
                    message="Authentication failed",
                    message_code=AUTH_FAILED,
                    status=StatusCode.UNAUTHORIZED
                )
        return catcher
    return decorator
