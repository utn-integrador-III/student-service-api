"""
This file defines the message codes for multilanguage in the frontend
Using i18n standard, please check multilanguage folder to add or modify messages
assets/i18n/<lang>
"""

# Common Messages
OK_MSG = "OK_MSG"
CREATED_MSG = "CREATED_MSG"
NOT_FOUND_MSG = "NOT_FOUND_MSG"
CONFLICT_MSG = "CONFLICT_MSG"
UNPROCESSABLE_ENTITY_MSG = "UNPROCESSABLE_ENTITY_MSG"
INTERNAL_SERVER_ERROR_MSG = "INTERNAL_SERVER_ERROR_MSG"
SERVER_TIMEOUT_MSG = "SERVER_TIMEOUT_MSG"
NO_DATA = "NO_DATA"

# Common Validations Messages
INVALID_ID = "INVALID_ID"  # Invalid Id

# Health Validations Messages
HEALTH_NOT_FOUND = "HEALTH_NOT_FOUND"  # Health not found
HEALTH_SUCCESSFULLY = "HEALTH_SUCCESSFULLY"  # Health successfully responded

# ZONE Validations Messages
ZONE_NOT_FOUND = "ZONE_NOT_FOUND"  # Zone not found
ZONE_SUCCESSFULLY_UPDATED = "ZONE_SUCCESSFULLY_UPDATED"  # Zone successfully updated
ZONE_SUCCESSFULLY_DELETED = "ZONE_SUCCESSFULLY_DELETED"  # Zone successfully deleted
ZONE_SUCCESSFULLY_CREATED = "ZONE_SUCCESSFULLY_CREATED"  # Zone created successfully
ZONE_DELETE_HAS_RELATIONS = "ZONE_DELETE_HAS_RELATIONS"  # Zone cannot be deleted, has relationships with some categories
ZONE_ALREADY_EXIST = "ZONE_ALREADY_EXIST"  # Zone already exist from database
ZONE_NAME_REQUIRED = "ZONE_NAME_REQUIRED"  # Requerid zone name
ZONE_LOCATION_REQUIRED = "ZONE_LOCATION_REQUIRED"  # Requerid zone location

ZONE_NOT_FOUND = 'ZONE_NOT_FOUND' # Zone not found
ZONE_SUCCESSFULLY_UPDATED = "ZONE_SUCCESSFULLY_UPDATED" # Zone successfully updated
ZONE_SUCCESSFULLY_DELETED = "ZONE_SUCCESSFULLY_DELETED" # Zone successfully deleted
ZONE_SUCCESSFULLY_CREATED = "ZONE_SUCCESSFULLY_CREATED" # Zone created successfully
ZONE_DELETE_HAS_RELATIONS = "ZONE_DELETE_HAS_RELATIONS" # Zone cannot be deleted, has relationships with some categories
ZONE_ALREADY_EXIST = 'ZONE_ALREADY_EXIST' #Zone already exist from database
ZONE_NAME_REQUIRED = 'ZONE_NAME_REQUIRED' # Requerid zone name
ZONE_LOCATION_REQUIRED = 'ZONE_LOCATION_REQUIRED' #Requerid zone location
INCORRECT_REQUEST_PARAM='COLUMN_NOT_FOUND'

LOST_OBJECTS_NOT_FOUND = 'LOST_OBJECTS_NOT_FOUND' 
LOST_OBJECTS_SUCCESSFULLY_CREATED = 'LOST_OBJECTS_SUCCESSFULLY_CREATED' 
LOST_OBJECTS_EXIST = 'LOST_OBJECTS_EXIST' 
LOST_OBJECTS_NAME_REQUIRED = 'LOST_OBJECTS_NAME_REQUIRED'
LOST_OBJECTS_DESCRIPTION_REQUIRED = 'LOST_DESCRIPTION_NAME_REQUIRED' 
INVALID_EMAIL_DOMAIN = 'INVALID_EMAIL_DOMAIN' 

# CATEGORY Validation Messages
CATEGORY_NOT_FOUND = "CATEGORY_SUCCESFULLY_UPDATED"
CATEGORY_SUCCESFULLY_UPDATED = "CATEGORY_SUCCESFULLY_UPDATED"
CATEGORY_SUCCESFULLY_DELETED = "CATEGORY_SUCCESFULLY_DELETED"
CATEGORY_SUCCESFULLY_CREATED = "CATEGORY_SUCCESFULLY_CREATED"
CATEGORY_DELETE_HAS_RELATIONS = "CATEGORY_DELETE_HAS_RELATIONS"
CATEGORY_ALREADY_EXISTS = "CATEGORY_ALREADY_EXISTS"
CATEGORY_NAME_REQUIRED = "CATEGORY_NAME_REQUIRED"
