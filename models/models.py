from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Define models (move later)
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    sender = Column(String)
    send_to = Column(String)

    def __init__(self, text, sender, send_to):
        self.text = text
        self.sender = sender
        self.send_to = send_to