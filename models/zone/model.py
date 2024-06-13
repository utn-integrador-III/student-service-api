from models.zone.db_queries import __dbmanager__
class ZoneModel():

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
        try:
            return __dbmanager__.get_by_id(id)
        except Exception as ex:
            raise Exception(f"Error fetching zone by id {id}: {ex}")
