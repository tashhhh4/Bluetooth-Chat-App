""" The responsibility of this 'service' is to tie message transport
    logic together with database operations in one place, and to keep
    backend logic out of the frontend while also keeping frontend
    logic out of the backend.

    Is this the 'protocol' layer?
"""

import json
import logging
from typing import LiteralString
from dataclasses import dataclass
from db.manager import chats, devices, members, messages, settings
from utils import EventRegistry, schedule
from messenger.utils import change_page

@dataclass
class Message:
    text: str

    def to_dict(self):
        return {'text': self.text}

@dataclass
class MessageObject:
    message: Message | None
    sender_uuid: str
    role: LiteralString['message', 'connection']

    def to_dict(self):
        message = self.message.to_dict() if self.message else None
        return {'message': message, 'sender_uuid': self.sender_uuid, 'role': self.role}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data):
        message_dict = json.loads(data)
        message = None
        if message_dict['message'] is not None:
            message = Message(
                text=message_dict['message']['text'],
            )
        message_obj = MessageObject(
            message=message,
            sender_uuid=message_dict['sender_uuid'],
            role=message_dict['role'],
        )
        return message_obj

INDENT = '                           '

class MessageService:

    def __init__(self, bluetooth_service):

        self.connection = None

        self.connected_state = ''
        self.connected_device = None

        self.event_registry = EventRegistry(
            [
                'MESSAGE_RECEIVED',
                'DEVICE_CONNECTED',
                'DEVICE_DISCONNECTED',
            ],
            'MessageService.EventRegistry'
        )

        self.bluetooth_service = bluetooth_service
        self.bluetooth_service.event_registry.register_event_callback('CONNECTION_ESTABLISHED', self._handle_device_connected)

        # self.bluetooth_service.event_registry.register_event_callback('CONNECTION_LOST', self._handle_device_disconnected)
        self.bluetooth_service.connection.event_registry.register_event_callback(
            'CONNECTION_LOST', self._handle_device_disconnected
        )

        self.bluetooth_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)

    # Message API
    @staticmethod
    def get_chat_for_device(device_uuid):
        existing_chats = chats.list_chats(device_uuid=device_uuid)
        if not existing_chats:
            raise RuntimeError(f'MessageService: No Chat with Device {device_uuid} found.')
        if len(existing_chats) > 1:
            logging.warning((f'MessageService: more than 1 chat with Device {device_uuid} '
                             'exists and multiple Chat channels with the same Device are not supported.'))
        return existing_chats[0]

    @staticmethod
    def get_device_for_chat(chat_id):
        devices_in_chat = members.list_devices(chat_id)
        if not devices_in_chat:
            raise RuntimeError(f'MessageService: No Device found in Chat #{chat_id}.')
        if len(devices_in_chat) > 1:
            logging.warning((f'More than 1 external Device found in Chat #{chat_id}, '
                             'but group chats are not supported.'))
        return devices_in_chat[0]

    def send_message(self, text, chat_id):
        """ Does socket message using the active BluetoothService.
            If there is an exception during transport,
            the message will not be added to the database.
        """
        try:
            # Database part - Get Device Records
            my_device = devices.get_mine()

            # Transport part
            message_obj = MessageObject(
                message=Message(text=text),
                sender_uuid=my_device.uuid,
                role='message',
            )
            message_json = message_obj.to_json()
            self.bluetooth_service.send_bytes(message_json)

            # Database part - Add message
            messages.create(chat_id, my_device.uuid, text)
        except Exception as e:
            logging.error(f'MessageService Error: {e}')

    @staticmethod
    def load_messages(chat_id):
        """ Returns messages as {'text': str, 'sender': str, 'time': str} """
        messages_in_chat = messages.list_messages(chat_id)
        frontend_messages = []
        for message_model in messages_in_chat:
            device = devices.get(message_model.device_uuid)
            if not device:
                device_name = 'No Device'
            elif device.name is None or device.name == '':
                device_name = 'Unknown Device'
            else:
                device_name = device.name
            message = {
                'text': message_model.text,
                'sender': device_name,
                'time': str(message_model.datetime),
            }
            frontend_messages.append(message)
        return frontend_messages

    @staticmethod
    def load_chats():
        """ Returns all your chats in a list. """
        chat_list = chats.list_chats()
        return chat_list

    def connect_to_device(self, address):
        self.bluetooth_service.connect_to_device(address)

    def open_chat_view(self, chat_id):
        chat = chats.get(chat_id)
        device = self.get_device_for_chat(chat_id)
        change_page('Chat', chat_id=chat.id, chat_title=chat.title, peer_device=device)

    # Handlers
    def _handle_device_connected(self):
        logging.info('[MessageService] Running _handle_device_connected()')

        # Send Connection Message
        my_device_uuid = settings.get_device_uuid()
        connection_message = MessageObject(message=None, sender_uuid=my_device_uuid, role='connection')
        connection_message_json = connection_message.to_json()
        logging.info(f'MessageService: Sending connection message to remote device: {connection_message_json}')
        self.bluetooth_service.send_bytes(connection_message_json)

    def _handle_device_disconnected(self):
        logging.info('[MessageService] Disconnected from remote device.')
        self.connected_state = 'DISCONNECTED'
        self.connected_device = None
        self.event_registry.emit_event('DEVICE_DISCONNECTED')

    def _handle_message_received(self, data):
        logging.info('[MessageService] Running _handle_message_received()')

        message_obj = MessageObject.from_json(data)
        logging.info(('MessageService: Converted message from JSON string to Python Object.\n'
                      f'{INDENT}{message_obj.__repr__()}'))

        if message_obj.role == 'message':
            logging.info('MessageService: Regular communication message received.')
            self._handle_message_message_received(message_obj)

        elif message_obj.role == 'connection':
            logging.info('MessageService: Connection initiation message received.')
            self._handle_connection_message_received(message_obj)

    def _handle_connection_message_received(self, message_obj):
        logging.info('MessageService: Running _handle_connection_message_received()')

        # Database - Add Device if unknown
        sender_device = devices.get(message_obj.sender_uuid)

        if not sender_device:
            logging.info('MessageService: New Device discovered.')

            remote_device_obj = self.bluetooth_service.connected_socket.getRemoteDevice()

            sender_device = devices.create(
                device_uuid=message_obj.sender_uuid,
                name=remote_device_obj.name,
                address=remote_device_obj.address,
            )
            logging.info(('MessageService: Created new Device record.\n'
                          f'{INDENT}{sender_device.__repr__()}'))
        else:
            logging.info(('MessageService: Connection message was from a known Device.\n'
                          f'{INDENT}{sender_device.__repr__()}'))

        # Own State - Set Connected Device, connected state, and notify subscribers
        self.connected_device = sender_device
        self.connected_state = 'CONNECTED'
        self.event_registry.emit_event('DEVICE_CONNECTED')

        # Database - Create chat with device if not exists
        existing_chats = chats.list_chats(device_uuid=message_obj.sender_uuid)
        if existing_chats:
            logging.info('MessageService: Retrieved previous Chat with peer Device.')
            target_chat = existing_chats[0]
            if len(existing_chats) > 1:
                logging.warning((f'MessageService: more than 1 chat with Device {sender_device.name} '
                      'exists and multiple Chat channels with the same Device are not yet supported.'))
        else:
            target_chat = chats.create([message_obj.sender_uuid])
            logging.info('MessageService: New Chat created.')
        logging.debug(f'MessageService: Target Chat set to {target_chat.__repr__()}')

        # Frontend - Jump into Chat View
        schedule(lambda _: self.open_chat_view(target_chat.id))

    def _handle_message_message_received(self, message_obj):
        logging.info('MessageService: Running _handle_message_message_received()')

        # Database - Retrieve Sender Device
        sender_device = devices.get(message_obj.sender_uuid)
        if not sender_device:
            logging.error(('MessageService: Received a Message from an unknown Device. This should probably not be '
                           'possible if the devices connected to each other before trying to send a normal message.'))
            return
        logging.debug(('MessageService: Successfully retrieved sender Device record.\n'
                     f'{INDENT}{sender_device.__repr__()}'))

        # Database - Retrieve Target Chat
        target_chat = self.get_chat_for_device(sender_device.uuid)

        logging.debug(('MessageService: Successfully retrieved the target Chat record.\n'
                      f'{INDENT}{target_chat.__repr__()}'))

        # Database - Insert message content
        new_message = messages.create(
            chat_id=target_chat.id,
            device_uuid=sender_device.uuid,
            text=message_obj.message.text,
        )
        logging.info(('MessageService: Created new Message record.\n'
                      f'{INDENT}{new_message.__repr__()}'))

        # Frontend - emit message received event
        self.event_registry.emit_event('MESSAGE_RECEIVED')
