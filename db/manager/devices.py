import uuid
from models import Device, Setting
from db.engine import get_session
from db.manager import settings

def create_mine(name, address):
    """ Initializes and adds the Device running this instance of Blu2. """
    with get_session() as session:
        my_uuid = uuid.uuid4()
        my_device_uuid_setting = Setting(key='MY_DEVICE_UUID', value=str(my_uuid))
        device = Device(uuid=str(my_uuid), address=address, name=name)
        session.add(device)
        session.add(my_device_uuid_setting)
        session.commit()
        return device

def create(device_uuid, name, address, owner=None):
    """ Add a Device discovered on the network. """
    with get_session() as session:
        device = Device(uuid=device_uuid, name=name, address=address, owner=owner)
        session.add(device)
        session.commit()
        return device

def list_devices():
    """ Lists known Devices, along with their owners if known. """
    with get_session() as session:
        return session.query(Device).all()

def get(device_uuid):
    """ Returns a single Device by uuid. """
    with get_session() as session:
        return session.get(Device, device_uuid)

def get_mine():
    """ Gets the Device that represents the Device running this instance of the app.
        The first time the app is run, this function will create the record for MY_DEVICE_UUID.
    """
    with get_session() as session:
        device_uuid = settings.get_device_uuid()
        my_device = session.get(Device, device_uuid)
        if my_device is None:
            session.add(Device(uuid=device_uuid, name='My Device'))
            session.commit()
            my_device = session.get(Device, device_uuid)
        return my_device

def update(device_uuid, name=None, owner=None, remove_owner=False):
    """ Update the name or owner of a Device. """
    with get_session() as session:
        device = session.get(Device, device_uuid)
        if name:
            device.name = name
        if owner:
            device.owner = owner
        if owner is None and remove_owner is True:
            device.owner = None
        # ... update connection information ...
        session.commit()
        return device

def delete_device(uuid):
    """ Forget a Device. """
    with get_session() as session:
        device = session.get(Device, uuid)
        deleted_id = device.uuid
        session.delete(device)
        session.commit()
        return deleted_id
