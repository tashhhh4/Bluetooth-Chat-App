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
