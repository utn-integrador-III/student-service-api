from db.mongo_client import Connection
from decouple import config

__dbmanager__ = Connection(config('ZONE_COLLECTION'))
