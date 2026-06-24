from db.engine import get_session
from models import Chat, Device, Message

def create(chat_id, device_uuid, text):
    """ Create a Message, sent to a particular Chat, from a sender (Device) or self (NULL)
        automatically timestamped.
    """
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        device = session.get(Device, device_uuid)
        message = Message(chat=chat, device=device, text=text)
        session.add(message)
        session.commit()
        return message

def list_messages(chat_id):
    """ Get all of the Messages sent to a particular Chat. """
    with get_session() as session:
        chat = session.get(Chat, chat_id)
        return chat.messages

def update(id, text):
    """ Update the text content of a Message. """
    with get_session() as session:
        message = session.get(Message, id)
        message.text = text
        session.commit()
        return message

def delete(id):
    """ Delete a Message. """
    with get_session() as session:
        message = session.get(Message, id)
        deleted_id = message.id
        session.delete(message)
        session.commit()
        return deleted_id