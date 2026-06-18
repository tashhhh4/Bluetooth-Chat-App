from sqlalchemy.exc import InvalidRequestError
from db.engine import get_session
from models import Setting

""" Manager for the Settings model.

    The settings table is handled differently from the other models because
    each value tends to have a specific use case.
    
    In most cases the behavior is simply to get the value, but
    then if the value is not set, some specific behavior to initialize that
    value will be run, and specific errors relating to that value can also
    be handled here.
"""

def get_service_uuid():
    """ Returns a unique identifier to identify BLE advertisements originating from any Blu2 app instance. """
    with get_session() as session:
        service_uuid = session.get(Setting, 'SERVICE_UUID')
        if service_uuid is None:
            from env import SERVICE_UUID
            service_uuid = Setting(key='SERVICE_UUID', value=SERVICE_UUID)
            session.add(service_uuid)
            session.commit()
            service_uuid = session.get(Setting, 'SERVICE_UUID')
            return service_uuid.value
        return service_uuid.value