from db.engine import get_session
from models import Message

# Super simple CRUD functions - placeholder
def get_all():
    session = get_session()
    try:
        return session.query(Message).all()
    finally:
        session.close()

def add_new(text):
    session = get_session()
    try:
        message = Message(text=text, sender='John Snow', send_to='Anonymous')
        session.add(message)
        session.commit()
    finally:
        session.close()


# Message Operations
def create_message():
    """ Create a Message, sent to a particular Chat, from a sender (Device) or self (NULL)
        automatically timestamped.
    """

def list_messages():
    """ Get all of the Messages sent to a particular Chat. """

def update_message():
    """ Update the text content of a Message. """

def delete_message():
    """ Delete a Message. """