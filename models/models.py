from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Contact(Base):
    """ Represents a human known by the user. Can be manually created and associated with
        discovered devices, or (coming later) integrated with an existing contact list.
    """
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # picture = ... add a photo of your friend ...
    # system_contact = ... link the user's contacts app ...

class Device(Base):
    """ A Device (for now only Android devices are supported) discovered on the network.
        Saves information on how to reconnect to this device in the future, as well as
        who owns it, if applicable.
    """
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(ForeignKey('contacts.id'))
    # bluetooth_id ... or whatever I need here ...
    # MAC address
    # Hotspot?

class Chat(Base):
    """ A Chat is a room to contain Messages involving the user and one or more other devices. Multiple
        chats with the same Device or Contact are allowed, enabling the user to create as many channels
        for organization as they need.
    """
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    datetime = Column(DateTime(timezone=False), server_default=func.now())
    # picture = ... customize a pretty icon for this chat ...

class Message(Base):
    """ The Message is the focus of the chat app. The "sender" column represents another Device running Blu2
        that the user has discovered and connected with. If the "sender" column is NULL then the Message object
        was sent by the user.
    """
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    sender = Column(ForeignKey('devices.id'))
    send_to = Column(ForeignKey('chats.id'))
    datetime = Column(DateTime(timezone=False), server_default=func.now())