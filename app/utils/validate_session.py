from google.protobuf.json_format import MessageToDict
from ..services.bootstrap import service_bus
from bson import objectid

def is_auth(token, scope):
    service_bus.init_connection()
    auth = service_bus.receive('validate_session', { 'authToken': token, 'scope': scope })
    service_bus.stop()
    service_bus.close_connection()

    if not objectid.ObjectId.is_valid(auth):
        raise Exception(auth) from None

    return auth
