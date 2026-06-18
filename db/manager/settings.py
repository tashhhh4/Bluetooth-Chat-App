from db.engine import get_session
from models import Setting

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

def list_all():
    """ Returns a list of all the Settings. """
    with get_session() as session:
        return session.query(Setting).all()

def delete(key):
    """ Deletes a Setting record by key. """
    with get_session() as session:
        record = session.get(Setting, key)
        session.delete(record)
        session.commit()