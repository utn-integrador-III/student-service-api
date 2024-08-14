from flask_restful import Api
from controllers.Lost_objects.controller import LostObjectsController
from controllers.Lost_objectsbyId.controller import LostObjectByIdController
from controllers.health.controller import HealthController
from controllers.zone.controller import ZoneController
from controllers.zonebyId.controller import ZoneByIdController
from controllers.category.controller import CategoryController
from controllers.categorybyId.controller import CategoryByIdController
from controllers.safekeeper.controller import SafekeeperController

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
    api.add_resource(LostObjectsController, LostObjectsController.route)
    api.add_resource(LostObjectByIdController, LostObjectByIdController.routeById)
    
    #SafeKeeper
    api.add_resource(SafekeeperController, SafekeeperController.route)

