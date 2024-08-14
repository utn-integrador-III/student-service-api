from models.safekeeper.db_queries import __dbmanager__

class SafekeeperModel:
    @classmethod
    def getAll(cls):
        try:
            info_db = []
            response = __dbmanager__.get_all_data()
            for info in response:
                try:
                    info_db.append(info)
                except Exception as ex:
                    raise Exception(ex)
            return info_db
        except Exception as ex:
            raise Exception(ex)