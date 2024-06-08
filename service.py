from flask_restful import Resource
from controllers.health.controller import HealthController
from controllers.Lost_objects.controller import LostObjectsController


from flask_restful import Api

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Zone
    # api.add_resource(Zone, Zone.route)
    # api.add_resource(ZoneById, ZoneById.route)
    
    # Object Lost
    api.add_resource(LostObjectsController, LostObjectsController.route) #Aqui se incluye el nuevo endpoind de objetos perdidos

    # api.add_resource(Report, Area.route)
    # api.add_resource(ReportById, ReportById.route)
    # api.add_resource(ReportByFilters, ReportByFilters.route)
    
