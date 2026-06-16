from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Setup
Base = declarative_base()
engine = create_engine('sqlite:///b2.data')

# Define Models (move later)
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    sender = Column(String)
    send_to = Column(String)

    def __init__(self, text, sender='MYSELF', send_to=None):
        self.text = text
        self.sender = sender
        self.send_to = send_to


Session = sessionmaker(bind=engine)
session = Session()

# Run
def reset_database():
    """ Creates the tables of the database based on the ORM model.
        *****************************
        DESTROYS ALL EXISTING DATA!!!
        *****************************
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Add some messages (placeholder)
    message_1 = Message(
        'I\'m sitting in 45a. Wanna trade seats? I can offer you some peanuts.',
        'Galaxy 500SE',
    )
    message_2 = Message(
        'Hi, how are you?',
        'Joe',
    )
    message_3 = Message(
        'Can you come to my seat, honey? The baby is getting hungry.',
        'Husband',
    )
    session.add(message_1)
    session.add(message_2)
    session.add(message_3)
    session.commit()

#reset_database()

# CRUD interface (placeholder)
def get_all_messages():
    messages = session.query(Message).all()
    return messages

def add_new_message(text):
    new_message = Message(
        text,
        sender='The Cat in the Hat'
    )
    session.add(new_message)
    session.commit()