from pymongo import MongoClient, errors
from bson import ObjectId
from models.lost_objects.db_queries import __dbmanager__
from bson.errors import InvalidId  # Import InvalidId class
from datetime import datetime
import logging
import pytz


class LostObjectModel():

    def __init__(self, name=None, description=None, status='Pending', attachment_path='/lostObjects', creation_date=None, claim_date=None, claimer="", safekeeper=None, _id=None):
        self.name = name
        self.description = description
        self.status = status
        self.attachment_path = attachment_path
        self.creation_date = creation_date if creation_date else datetime.now(pytz.timezone('America/Costa_Rica')).replace(tzinfo=None)
        self.claim_date = claim_date
        self.claimer = claimer
        self.safekeeper = safekeeper if safekeeper else []
        self._id = _id

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "attachment_path": self.attachment_path,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,  
            "claim_date": self.claim_date.isoformat() if self.claim_date else None,  
            "claimer": self.claimer,
            "safekeeper": self.safekeeper,
        }

    # @classmethod
    def get_all():
        info_db = []
        response = __dbmanager__.get_all_data()    
        
        for info in response:
            try:
                info_db.append(info)
            except Exception as ex:
                raise Exception(ex)
        
        return info_db
    
    @classmethod
    def get_by_name(cls, name):
        try:
            # Buscar el objeto por nombre en la base de datos
            result = __dbmanager__.find_one({"name": name})
            if result:
                return cls(_id=result.get("_id"), name=result.get("name"), description=result.get("description"),
                           status=result.get("status"), attachment_path=result.get("attachment_path"),
                           creation_date=result.get("creation_date"), claim_date=result.get("claim_date"), 
                           claimer=result.get("claimer"), safekeeper=result.get("safekeeper"))
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get lost object by name: " + str(ex))
    
    @classmethod
    def create(cls, data):
        try:
            if 'creation_date' in data and isinstance(data['creation_date'], datetime):
                data['creation_date'] = data['creation_date'].replace(tzinfo=None)  # Remove timezone info for MongoDB
            if 'claim_date' in data and isinstance(data['claim_date'], datetime):
                data['claim_date'] = data['claim_date'].replace(tzinfo=None)  # Remove timezone info for MongoDB
            __dbmanager__.create_data(data)  # Insert data as a dictionary
            return cls(**data)
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create lost object: " + str(ex))
