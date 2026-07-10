from db.engine import get_session
from models import Chat, Device, Member

def create(device_id, chat_id):
    """ Adds a Device to a Chat. """
    with get_session() as session:
        device = session.get(Device, device_id)
        chat = session.get(Chat, chat_id)
        member = Member(device=device, chat=chat)
        session.add(member)
        session.commit()
        return member

def list_members(chat_id):
    """ Lists all the Members belonging to a particular Chat. """
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        return chat.members

def list_devices(chat_id):
    """ Lists all the Devices from the Members in the Chat. """
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        return chat.devices

def list_memberships(device_id):
    """ List all Chats in which a Device is found. """
    with get_session() as session:
        device = session.get(Device, device_id)
        return device.memberships

def delete(device_id, chat_id):
    """ Remove a Device from a Chat. """
    with get_session() as session:
        member = session.get(Member, {'device_id': device_id, 'chat_id': chat_id})
        session.delete(member)
        session.commit()
        return device_id, chat_id
