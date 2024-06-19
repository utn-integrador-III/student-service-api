from bson import ObjectId
from models.category.db_queries import __dbmanager__


class CategoryModel:

    def __init__(self, _id=None, category_name=None):
        self._id = _id
        self.category_name = category_name

    def to_dict(self):
        return {
            "category_name": self.category_name,
        }

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

    @classmethod
    def getById(cls, id):
        try:
            return __dbmanager__.get_by_id(id)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getByName(cls, name):
        try:
            result = __dbmanager__.find_one({"category_name": name})
            if result:
                return cls(_id=result.get("_id"), name=result.get("category_name"))
            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def create(cls, data):
        try:
            category = cls(**data)
            __dbmanager__.create_data(category.to_dict())
            return category
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update(cls, id, data):
        try:
            new_category_name = data.get("category_name")
            existing_category = cls.getByName(new_category_name)
            if existing_category and str(existing_category["_id"]) != id:
                return None
            result = __dbmanager__.update_data(id, data)
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete(cls, id):
        try:
            result = __dbmanager__.delete_data(id)
            if result:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
