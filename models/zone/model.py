from bson import ObjectId
from bson.errors import InvalidId  # Import InvalidId class
from models.zone.db_queries import __dbmanager__
import logging


class ZoneModel:

    @staticmethod
    def get_all():
        """
        Retrieve all zones from the database.
        """
        info_db = []
        try:
            response = __dbmanager__.get_all_data()
            for info in response:
                info_db.append(info)
        except Exception as ex:
            logging.error(f"Error fetching all zones: {ex}")
            raise Exception(f"Error fetching all zones: {ex}")

        return info_db

    @staticmethod
    def get_by_id(id):
        """
        Retrieve a zone by its ID.
        """
        try:
            # Ensure the id is a valid ObjectId
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            return __dbmanager__.get_by_id(id)
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            raise ex  # Re-raise InvalidId to handle it specifically in the get method
        except Exception as ex:
            logging.error(f"Error fetching zone by id {id}: {ex}")
            raise Exception(f"Error fetching zone by id {id}: {ex}")

    @staticmethod
    def delete(id):
        """
        Delete a zone by its ID.
        """
        try:
            # Ensure the id is a valid ObjectId
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            result = __dbmanager__.delete_data(str(id))
            return result
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            raise ex  # Re-raise InvalidId to handle it specifically in the delete method
        except Exception as ex:
            logging.error(f"Error deleting zone by id {id}: {ex}")
            raise Exception(f"Error deleting zone by id {id}: {ex}")
