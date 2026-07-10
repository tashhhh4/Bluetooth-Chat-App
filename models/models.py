from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
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
        who owns it, if applicable. Upon database creation, the user's own instance of the app
        generates a UUID to identify its own device, which is inserted as the first row in the
        "devices" table. If a Message comes from a Device matching the id of the user's own Device,
        That Message is shown in whatever special frontend formatting helps to distinguish it
    """
    __tablename__ = 'devices'

    uuid = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    owner = Column(ForeignKey('contacts.id'))

    memberships = relationship('Member', back_populates='device')
    messages = relationship('Message', back_populates='device')

    def __repr__(self):
        return f'Model Device(uuid=\'{self.uuid}\', name=\'{self.name}\', address=\'{self.address}\', owner={self.owner})'

    def __eq__(self, other):
        return self.uuid == other.uuid

class Chat(Base):
    """ A Chat is a room to contain Messages involving the user and one or more other devices. Multiple
        chats with the same Device or Contact are allowed, enabling the user to create as many channels
        for organization as they need. However a Chat must always have at least one Member (which is a
        Device apart from the user's own).
    """
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    datetime = Column(DateTime(timezone=False), server_default=func.now())
    # picture = ... customize a pretty icon for this chat ...

    members = relationship('Member', back_populates='chat', cascade='all, delete-orphan')
    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')
    devices = relationship('Device', secondary='chat_devices', viewonly=True, lazy='selectin')

    def __init__(self, devices):
        if not devices:
            raise ValueError('Chat requires at least one device.')
        self.title = ', '.join(d.name for d in devices)
        self.members = [Member(device=d) for d in devices]

    def __repr__(self):
        return f'Model Chat>(id={self.id}, title=\'{self.title}\', datetime=\'{self.datetime}\')'

class Member(Base):
    """ A Device which is a Member of a Chat. """
    __tablename__ = 'chat_devices'

    __table_args__ = (UniqueConstraint('device_uuid', 'chat_id'),)

    id = Column(Integer, primary_key=True)
    device_uuid = Column(ForeignKey('devices.uuid', ondelete='CASCADE'))
    chat_id = Column(ForeignKey('chats.id', ondelete='CASCADE'))

    device = relationship('Device', back_populates='memberships')
    chat = relationship('Chat', back_populates='members')

class Message(Base):
    """ The Message is the focus of the chat app. The "device_uuid" column represents another Device running Blu2
        which sent the Message. "device_id" can also be NULL, meaning that the Message is the user's own.
        The "chat_id" column represents the Chat to which the Message will be sent.
    """
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    device_uuid = Column(ForeignKey('devices.uuid'))
    chat_id = Column(ForeignKey('chats.id', ondelete='CASCADE'))
    datetime = Column(DateTime(timezone=False), server_default=func.now())

    device = relationship('Device', back_populates='messages')
    chat = relationship('Chat', back_populates='messages')

    def __repr__(self):
        return (f'Model Message(id={self.id}, text=\'{self.text}\', device_uuid=\'{self.device_uuid}\', '
                'chat_id={self.chat_id}, datetime=\'{self.datetime}\'')

class Setting(Base):
    """" Application-level settings as key-value pairs. """
    __tablename__ = 'settings'

    key = Column(String, primary_key=True)
    value = Column(String)