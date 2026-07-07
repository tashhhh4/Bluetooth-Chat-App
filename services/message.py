""" The responsibility of this 'service' is to tie message transport
    logic together with database operations in one place, and to keep
    as much logic and complexity out of the 'frontend' as possible.

    Is this the 'protocol' layer?
"""

import json
import logging
from dataclasses import dataclass
from db.manager import chats, devices, messages, settings
from utils import EventRegistry, schedule
from messenger.utils import change_page

@dataclass
class Message:
    text: str
    chat_id: int

    def to_dict(self):
        return {'text': self.text, 'chat_id': self.chat_id}

@dataclass
class MessageObject:
    message: Message | None
    sender_uuid: str

    def to_dict(self):
        message = self.message.to_dict() if self.message else None
        return {'message': message, 'sender_uuid': self.sender_uuid}

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data):
        message_dict = json.loads(data)
        message = None
        if message_dict['message'] is not None:
            message = Message(
                text=message_dict['message']['text'],
                chat_id=message_dict['message']['chat_id']
            )
        message_obj = MessageObject(message=message, sender_uuid=message_dict['sender_uuid'])
        return message_obj


class MessageService:

    event_registry = EventRegistry(
        ['MESSAGE_RECEIVED'],
        'MessageService.event_registry'
    )
    bluetooth_service = None

    def __init__(self, bluetooth_service):

        self.bluetooth_service = bluetooth_service
        self.bluetooth_service.event_registry.register_event_callback('CONNECTION_ESTABLISHED', self._handle_device_connected)

        # Whenever the BluetoothService emits the MESSAGE_RECEIVED event,
        # the MessageService runs its own _handle_message_received function,
        # which also emits a MESSAGE_RECEIVED event from MessageService
        self.bluetooth_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)

    # Message API
    def send_message(self, text, chat_id):
        """ Does socket message using the active BluetoothService.
            If there is an exception during transport,
            the message will not be added to the database.
        """
        my_device_uuid = settings.get_device_uuid()
        try:
            # Transport part
            message_obj = MessageObject(
                message=Message(text=text, chat_id=chat_id),
                sender_uuid=my_device_uuid
            )
            message_json = message_obj.to_json()
            self.bluetooth_service.send_bytes(message_json)

            # Database part
            messages.create(chat_id, my_device_uuid, text)
        except Exception as e:
            print('MessageService Error:', e)

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

    # Handlers
    def _handle_device_connected(self):
        logging.info('[MessageService] Running _handle_device_connected()')

        # Self Introduction Over Bluetooth
        my_device_uuid = settings.get_device_uuid()
        self_intro = MessageObject(message=None, sender_uuid=my_device_uuid)
        self_intro_json = self_intro.to_json()
        logging.info(f'MessageService: Sending self introduction message to remote device: {self_intro_json}')
        self.bluetooth_service.send_bytes(self_intro_json)

    def _handle_message_received(self, data):
        logging.info('[MessageService] Running _handle_message_received()')

        message_obj = MessageObject.from_json(data)
        logging.info(('MessageService: Converted message from JSON string to Python Object.\n'
                      f'                           {message_obj.__repr__()}'))

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
                          f'                           {sender_device.__repr__()}'))
        else:
            logging.info(('MessageService: Message is from a known Device.\n'
                          f'                           {sender_device.__repr__()}'))

        # Database - Create chat with device if not exists

        # So yes, I ONLY want to pop into the Chat View when the connected_socket becomes connected.

        existing_chats = chats.list_chats(device_uuid=message_obj.sender_uuid)
        if not existing_chats:
            target_chat = chats.create([message_obj.sender_uuid])
            logging.info(('MessageService: New Chat created.\n'
                          f'                           {target_chat.__repr__()}'))
        else:
            target_chat = existing_chats[0]
        if len(existing_chats) > 1:
            print('Warning: more than 1 chat with Device', sender_device.name,
                  'exists and multiple Chat channels with the same Device are not yet supported.')

        # Frontend - Jump into Chat View with Chat object
        # (will currently happen on EVERY single message but I will optimize it later)
        def go(_):
            change_page('Chat', chat_id=target_chat.id, chat_title=target_chat.title)
        schedule(go)

        # Database - Add message content
        if message_obj.message:
            messages.create(
                chat_id=message_obj.message.chat_id,
                device_uuid=sender_device.uuid,
                text=message_obj.message.text,
            )

        # Frontend - emit message received event
        if message_obj.message:
            self.event_registry.emit_event('MESSAGE_RECEIVED', message_obj.message.text)

