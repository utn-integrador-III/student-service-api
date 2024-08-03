from functools import wraps
import requests
from flask import request
from utils.server_response import *
from utils.message_codes import *
from decouple import config
import logging

def auth_required(action=None, permission='', with_args=False):
    def decorator(f):
        @wraps(f)
        def catcher(*args, **kwargs):
            try:
                token = request.headers["Authorization"]
            except KeyError:
                return {'message': "Authorization token is required"}, 401

            try:
                # Send Permission to verify if the user has authorization
                body = {'permission': permission}
                response = requests.post(
                    f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/auth/verify_auth",
                    json=body,
                    headers={'Authorization': token},
                    timeout=20
                )
            except Exception as ex:
                logging.error(f"Error in authentication request: {str(ex)}")
                return {'message': f"Error in authentication occurred: {str(ex)}"}, 500

            if response.status_code == 200:
                try:
                    if response.content:
                        response_data = response.json()
                    else:
                        logging.error(f"Auth service returned an empty response")
                        return {'message': "Invalid response from auth service"}, 500
                    
                    name = response_data["data"]["rolName"]
                    
                    bodyRole = {'name': name}
                    # Make request to security API to check role permissions
                    role_response = requests.get(
                        f"{config('AUTH_API_URL')}:{config('AUTH_API_PORT')}/rol",
                        json=bodyRole,
                    )

                    if role_response.status_code == 200:
                        if role_response.content:
                            role_response_data = role_response.json()
                            print(role_response_data)
                        else:
                            logging.error(f"Security service returned an empty response")
                            return {'message': "Invalid response from security service"}, 500
                        
                        role_permissions = role_response_data["data"]["permissions"]
                        if permission in role_permissions:
                            if with_args:
                                kwargs['current_user'] = response_data["data"]
                            return f(*args, **kwargs)
                        else:
                            return {'message': "Permission denied"}, 403
                    else:
                        logging.error(f"Error verifying role permissions: {role_response.content}")
                        return {'message': "Error verifying role permissions"}, 500
                except Exception as ex:
                    logging.error(f"Error processing authentication response: {str(ex)}")
                    return {'message': f"Error processing authentication response: {str(ex)}"}, 500
            else:
                if response.content:
                    try:
                        return response.json(), 401
                    except Exception as ex:
                        logging.error(f"Error decoding JSON response: {str(ex)}, Response content: {response.content}")
                        return {'message': "Invalid response format from auth service"}, 500
                else:
                    logging.error(f"Auth service returned an empty response")
                    return {'message': "Invalid response from auth service"}, 500
        return catcher
    return decorator
