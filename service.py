from flask_restful import Resource
from controllers.Lost_objects.controller import LostObjectsController
from controllers.lost_objectsbyid.controller import LostObjectByIdController
from controllers.health.controller import HealthController
from controllers.zone.controller import ZoneController
from controllers.zonebyId.controller import ZoneByIdController
from controllers.category.controller import CategoryController
from controllers.categorybyId.controller import CategoryByIdController
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

    # Object Lost
    api.add_resource(LostObjectsController, LostObjectsController.route)
    api.add_resource(LostObjectByIdController, LostObjectByIdController.routeById)

    # api.add_resource(Report, Area.route)
    # api.add_resource(ReportById, ReportById.route)
    # api.add_resource(ReportByFilters, ReportByFilters.route)
