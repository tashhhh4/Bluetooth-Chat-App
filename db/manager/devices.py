from db.engine import get_session
from models import Device

def create_device(name, owner=None):
    """ Add a new Device. """
    session = get_session()
    try:
        device = Device(name=name, owner=owner)
        # ... bluetooth_address ...
        session.add(device)
        session.commit()
        return device
    finally:
        session.close()

def list_devices():
    """ Lists known Devices, along with their owners if known. """
    session = get_session()
    try:
        return session.query(Device).all()
    finally:
        session.close()

def update_device(name=None, owner=None, remove_owner=False):
    """ Update the name or owner of a Device. """
    session = get_session()
    try:
        device = session.get(Device, id)
        if name:
            device.name = name
        if owner:
            device.owner = owner
        if owner is None and remove_owner is True:
            device.owner = None
        # ... update connection information ...
        session.update(device)
        session.commit()
        return device
    finally:
        session.close()

def delete_device(id):
    """ Forget a Device. """
    session = get_session()
    try:
        device = session.get(Device, id)
        session.delete(device)
        session.commit()
        return device
    finally:
        session.close()
