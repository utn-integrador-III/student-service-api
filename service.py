from flask_restful import Resource
from controllers.Lost_objects.controller import LostObjectsController
from controllers.health.controller import HealthController
from controllers.zone.controller import ZoneController
from controllers.zonebyId.controller import ZoneByIdController


from flask_restful import Api

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Zone
    api.add_resource(ZoneController, ZoneController.route)
    api.add_resource(ZoneByIdController, ZoneByIdController.route)
    
    # Object Lost
    api.add_resource(LostObjectsController, LostObjectsController.route)

    # api.add_resource(Report, Area.route)
    # api.add_resource(ReportById, ReportById.route)
    # api.add_resource(ReportByFilters, ReportByFilters.route)
    
