import uuid
from db.engine import get_session
from models import Device, Setting

def create_my_device(name, address):
    """ Initializes and adds the Device running this instance of Blu2. """
    with get_session() as session:
        my_uuid = uuid.uuid4()
        my_device_uuid_setting = Setting(key='MY_DEVICE_UUID', value=str(my_uuid))
        device = Device(uuid=str(my_uuid), address=address, name=name)
        session.add(device)
        session.add(my_device_uuid_setting)
        session.commit()
        return device

def create_device(device_uuid, name, address, owner=None):
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

def get_my_device():
    """ Gets the Device that represents the Device running this instance of the app.
        The first time the app is run, this function will create the record for MY_DEVICE_ID.
    """
    with get_session() as session:
        device_id = session.get(Setting, 'MY_DEVICE_ID')
        print('device_id is', device_id)

def update_device(uuid, name=None, owner=None, remove_owner=False):
    """ Update the name or owner of a Device. """
    with get_session() as session:
        device = session.get(Device, uuid)
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
