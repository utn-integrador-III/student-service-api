from models.zone.db_queries import __dbmanager__
import logging


class ZoneModel:

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
    def delete(cls, id):
        try:
            result = __dbmanager__.delete_data(str(id))
        except Exception as ex:
            # logging.exception(ex)
            raise Exception(ex)
