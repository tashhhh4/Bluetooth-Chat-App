""" The responsibility of this 'service' is to tie message transport
    logic together with database operations in one place, and to keep
    as much logic and complexity out of the 'frontend' as possible.

    Is this the 'protocol' layer?
"""
# The ChatView should only load the chat and display the messages.

# The MessageService should decide which chat to give the Chat View.
# The MessageService not the BluetoothService should decide when to pop the Chat View into the user's face.

import json
from dataclasses import dataclass
from db.manager import chats, devices, messages, settings
from utils import device_java_obj_to_dict, EventRegistry, schedule
from messenger.utils import change_page

FAKE_CHAT_ID = '1' # manually create with debug interface

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

    def send_message(self, text):
        """ Does socket message using the active BluetoothService.
            If there is an exception during transport,
            the message will not be added to the database.
        """
        my_device_uuid = settings.get_device_uuid()
        try:
            # Transport part
            message_obj = MessageObject(
                message=Message(text=text, chat_id=FAKE_CHAT_ID),
                sender_uuid=my_device_uuid
            )
            message_json = message_obj.to_json()
            self.bluetooth_service.send_bytes(message_json)

            # Database part
            messages.create(FAKE_CHAT_ID, my_device_uuid, text)
        except Exception as e:
            print('MessageService.send_message:', e)

    def _handle_device_connected(self):
        print('MessageService._handle_device_connected: running.')

        # Self Introduction Over Bluetooth
        my_device_uuid = settings.get_device_uuid()
        self_intro = MessageObject(message=None, sender_uuid=my_device_uuid)
        self_intro_json = self_intro.to_json()
        self.bluetooth_service.send_bytes(self_intro_json)

    def _handle_message_received(self, data):

        message_obj = MessageObject.from_json(data)

        # Database - Add Device if unknown
        sender_device = devices.get(message_obj.sender_uuid)

        if not sender_device:
            print('Device unknown. Adding new record...')

            remote_device_obj = self.bluetooth_service.connected_socket.getRemoteDevice()

            devices.create(
                device_uuid=message_obj.sender_uuid,
                name=remote_device_obj.name,
                address=remote_device_obj.address,
            )
            sender_device = devices.get(message_obj.sender_uuid)

        # Database - Create chat with device if not exists
        existing_chats = chats.list_chats(device_uuid=message_obj.sender_uuid)
        if len(existing_chats) > 1:
            print('Warning: more than 1 chat with Device', sender_device.name, 'exists and multiple Chat channels with the same Device are not yet supported.')
        if not existing_chats:
            target_chat = chats.create([message_obj.sender_uuid])
        else:
            target_chat = existing_chats[0]

        # Frontend - Jump into Chat View with Chat object
        # (will currently happen on EVERY single message but I will optimize it later)
        device = self.bluetooth_service.connected_socket.getRemoteDevice()
        device_dict = device_java_obj_to_dict(device)
        def go(_):
            change_page('Chat', device=device_dict)
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

