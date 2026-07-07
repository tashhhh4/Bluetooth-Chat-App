from db.engine import get_session
from db.manager import devices
from models import Chat, Device, Member

def create(device_uuids):
    """ Creates a new Chat. A Chat must be initialized with at least 1 Device (-> Member) or else it's an error!
        (Currently the App does not support being used as a notepad.)
    """
    with get_session() as session:
        device_models = [devices.get(u) for u in device_uuids]
        chat = Chat(device_models)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

def list_chats(device_uuid=None):
    """ Lists all the user's Chats, optionally filtering by device. """
    with get_session() as session:
        if device_uuid:
            return (
                session.query(Chat)
                .filter(Chat.devices.any(Device.uuid == device_uuid))
                .all()
            )
        return session.query(Chat).all()

def get(id):
    """ Returns a Chat by id. """
    with get_session() as session:
        return session.get(Chat, id)

def update(id, title):
    """ Change the title of the Chat. """
    with get_session() as session:
        chat = session.get(Chat, id)
        chat.title = title
        session.update(chat)
        session.commit()
        return chat

def delete(id):
    """ Delete a Chat, along with all of its Messages, and all of its Member associations. """
    with get_session() as session:
        chat = session.get(Chat, id)
        deleted_id = chat.id
        session.delete(chat)
        session.commit()
        return deleted_id