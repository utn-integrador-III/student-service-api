from flask_restful import Resource
from controllers.Lost_objects.controller import LostObjectsListController, LostObjectsDetailController
from controllers.health.controller import HealthController
from controllers.zone.controller import ZoneController
from controllers.zonebyId.controller import ZoneByIdController
from controllers.category.controller import CategoryController, CategoryByIdController
from flask_restful import Api

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Zone
    api.add_resource(ZoneController, ZoneController.route)
    api.add_resource(ZoneByIdController, ZoneByIdController.route)

    # Category
    api.add_resource(CategoryController, CategoryController.route)
    api.add_resource(CategoryByIdController, CategoryByIdController.routeById)

    # Lost Objects
    api.add_resource(LostObjectsListController, LostObjectsListController.route)
    api.add_resource(LostObjectsDetailController, LostObjectsDetailController.route)
