


from distutils import errors
from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class

from models.zone.db_queries import __dbmanager__
import logging


class ZoneModel:

    def __init__(self, name=None, location=None, _id=None):
        self.name = name
        self.location = location
        self._id = _id

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
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
            # Search for the zone by name in the database
            result = __dbmanager__.find_one({"name": name})
            if result:
                return cls(_id=result.get("_id"), name=result.get("name"))
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get zone by name: " + str(ex))

    @classmethod
    def create(cls, data):
        try:
            zone = cls(**data)
            __dbmanager__.create_data(zone.to_dict())  # Insert data as a dictionary
            return zone
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create zone: " + str(ex))

    @classmethod
    def delete(cls, id):
        try:
            result = __dbmanager__.delete_data(str(id))
            if result:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, id):
        try:
            # Ensure the id is a valid ObjectId
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            return __dbmanager__.get_by_id(id)
        except InvalidId as ex:
            raise ex  # Re-raise InvalidId to handle it specifically in the get method
        except Exception as ex:
            raise Exception(f"Error fetching zone by id {id}: {ex}")
    
    @classmethod
    def update(cls, id, update_data):
        if not isinstance(id, str) or not ObjectId.is_valid(id):
            raise ValueError("Invalid id value")

        id = ObjectId(id)
        result = __dbmanager__.update_data(id, update_data)
        if result:
            updated_zone = cls.get_by_id(str(id))
            return updated_zone
        else:
            return None


