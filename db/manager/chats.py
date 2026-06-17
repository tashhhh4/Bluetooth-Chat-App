from db.engine import get_session
from models import Chat, Member

def create_chat(devices):
    """ Creates a new Chat. A Chat must be initialized with at least 1 Device (-> Member) or else it's an error!
        (Currently the App does not support being used as a notepad.)
    """
    with get_session() as session:
        chat = Chat(devices)
        session.add(chat)
        session.commit()
        return chat

def list_chats():
    """ Lists all the user's Chats. """
    with get_session() as session:
        return session.query(Chat).all()

def update_chat(id, title):
    """ Change the title of the Chat. """
    with get_session() as session:
        chat = session.get(Chat, id)
        chat.title = title
        session.update(chat)
        session.commit()
        return chat

def delete_chat(id):
    """ Delete a Chat, along with all of its Messages, and all of its Member associations. """
    with get_session() as session:
        chat = session.get(Chat, id)
        deleted_id = chat.id
        session.delete(chat)
        session.commit()
        return deleted_id