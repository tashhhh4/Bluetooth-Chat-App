from db.engine import get_session
from models import Setting

def get_service_uuid():
    """ Returns a unique identifier to identify BLE advertisements originating from any Blu2 app instance. """
    with get_session() as session:
        service_uuid = session.get(Setting, 'SERVICE_UUID')
        if service_uuid is None:
            from env import SERVICE_UUID
            new_setting = Setting(key='SERVICE_UUID', value=SERVICE_UUID)
            session.add(new_setting)
            session.commit()
            service_uuid = session.get(Setting, 'SERVICE_UUID')
            return service_uuid.value
        return service_uuid.value

def get_device_uuid():
    """ Returns the unique identifier of the user's own device.
        - Identifies the device on which this Blu2 app runs to other
          Blu2 app instances.
    """
    with get_session() as session:
        device_uuid = session.get(Setting, 'DEVICE_UUID')
        if device_uuid is None:
            from uuid import uuid4
            new_uuid = str(uuid4())
            new_setting = Setting(key='DEVICE_UUID', value=new_uuid)
            session.add(new_setting)
            session.commit()
            device_uuid = session.get(Setting, 'DEVICE_UUID')
            return device_uuid.value
        return device_uuid.value

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