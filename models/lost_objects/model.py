from pymongo import MongoClient, errors
from models.lost_objects.db_queries import __dbmanager__

class LostObjectModel():

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
