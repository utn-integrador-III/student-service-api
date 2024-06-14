from models.zone.db_queries import __dbmanager__
import logging


class ZoneModel:

    def __init__(self, name, location):
        self.name = name
        self.location = location

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
    
    # @classmethod
    def get_by_id(id):
        return []

    
    @classmethod
    def get_by_name(cls, name):
        try:
            result = __dbmanager__.find_one({"name": name})
            if result:
                return cls(**result)
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
        except Exception as ex:
            raise Exception(ex)

    
        # @classmethod
    def get_by_id(id):
        try:
            return __dbmanager__.get_by_id(id)
        except Exception as ex:
            raise Exception(f"Error fetching zone by id {id}: {ex}")

