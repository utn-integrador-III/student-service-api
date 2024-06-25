from pymongo import MongoClient, errors
from bson import ObjectId
from models.lost_objects.db_queries import __dbmanager__
from bson.errors import InvalidId  # Import InvalidId class
from datetime import datetime
import logging
import pytz


class LostObjectModel():

    def __init__(self, name=None, description=None, status='Pending', creation_date=None, attachment_path='/lostObjects', claim_date=None, claimer="", safekeeper=None, user_email=None, _id=None):
        self.name = name
        self.description = description
        self.status = status
        self.creation_date = creation_date if creation_date else datetime.now(pytz.timezone('America/Costa_Rica')).replace(tzinfo=None)
        self.attachment_path = attachment_path
        self.claim_date = claim_date
        self.claimer = claimer
        self.safekeeper = safekeeper if safekeeper else []
        self.user_email = user_email
        self._id = _id

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None, 
            "attachment_path": self.attachment_path, 
            "claim_date": self.claim_date.isoformat() if self.claim_date else None,  
            "claimer": self.claimer,
            "safekeeper": self.safekeeper,
            "user_email": self.user_email
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
            result = __dbmanager__.find_one({"name": name})
            if result:
                return cls(
                    _id=result.get("_id"), 
                    name=result.get("name"), 
                    description=result.get("description"),
                    status=result.get("status"), 
                    attachment_path=result.get("attachment_path"),
                    creation_date=result.get("creation_date"), 
                    claim_date=result.get("claim_date"), 
                    claimer=result.get("claimer"), 
                    safekeeper=result.get("safekeeper"),
                    user_email=result.get("user_email")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get lost object by name: " + str(ex))
    
    @classmethod
    def create(cls, data):
        try:
            if 'creation_date' in data and isinstance(data['creation_date'], datetime):
                data['creation_date'] = data['creation_date'].replace(tzinfo=None)  
            if 'claim_date' in data and isinstance(data['claim_date'], datetime):
                data['claim_date'] = data['claim_date'].replace(tzinfo=None)  

            reordered_data = {key: data[key] for key in data if key != 'user_email'}
            reordered_data['user_email'] = data['user_email']

            __dbmanager__.create_data(reordered_data) 
            return cls(**data)
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create lost object: " + str(ex))
