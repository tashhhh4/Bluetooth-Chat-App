""" The responsibility of this 'service' is to tie message transport
    logic together with database operations in one place, and to keep
    as much logic and complexity out of the 'frontend' as possible.

    Is this the 'protocol' layer?
"""

import json
from dataclasses import dataclass
from db.manager import messages
from db.manager import settings
from utils import EventRegistry

# temp
FAKE_DEVICE_UUID = '49cb8896-d78d-463f-9d10-7f115bbdd924'
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
            messages.create(FAKE_CHAT_ID, FAKE_DEVICE_UUID, text)
        except Exception as e:
            print('MessageService.send_message:', e)

    @staticmethod
    def _handle_device_connected():
        # bluetooth_service = get_bluetooth_service()
        print('This is MessageService. I know that you connected a new device. I have to stop you here and ask some questions, but I\'ll figure out how to do that in a hot minute.')

    def _handle_message_received(self, data):

        message_obj = json.loads(data)
        text = message_obj['message']['text']

        # Database part
        messages.create(FAKE_CHAT_ID, FAKE_DEVICE_UUID, text)

        # Frontend part
        self.event_registry.emit_event('MESSAGE_RECEIVED', text)