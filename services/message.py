""" The responsibility of this 'service' is to tie message transport
    logic together with database operations in one place, and to keep
    as much logic and complexity out of the 'frontend' as possible.

    Is this the 'protocol' layer?
"""

import json
from dataclasses import dataclass
from db.manager import messages
from utils import EventRegistry

# temp
FAKE_DEVICE_UUID = '49cb8896-d78d-463f-9d10-7f115bbdd924'
FAKE_CHAT_ID = '1' # manually create with debug interface

@dataclass
class Message:
    text: str
    chat_id: int

@dataclass
class MessageObject:
    message: Message | None
    sender_uuid: str

class MessageService:

    event_registry = EventRegistry(
        ['MESSAGE_RECEIVED'],
        'MessageService.event_registry'
    )
    bluetooth_service = None

    def __init__(self, bluetooth_service):
        bluetooth_service.event_registry.register_event_callback('CONNECTION_ESTABLISHED', self._handle_device_connected)

        # Whenever the BluetoothService emits the MESSAGE_RECEIVED event,
        # the MessageService runs its own _handle_message_received function,
        # which also emits a MESSAGE_RECEIVED event from MessageService
        bluetooth_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)

    def send_message(self, text):
        """ Does socket message using the active BluetoothService.
            If there is an exception during transport,
            the message will not be added to the database.
        """
        print('MessageService.send_message running.')
        try:
            # Transport part
            message = {'message': {'text': text}}
            message_json_str = json.dumps(message)
            self.bluetooth_service.send_bytes(message_json_str)

            # Database part
            messages.create(FAKE_CHAT_ID, FAKE_DEVICE_UUID, message['message']['text'])
        except Exception as e:
            print('MessageService.send_message:', e)

    @staticmethod
    def _handle_device_connected():
        # bluetooth_service = get_bluetooth_service()
        print('This is MessageService. I know that you connected a new device. I have to stop you here and ask some questions, but I\'ll figure out how to do that in a hot minute.')

    def _handle_message_received(self, data):
        # Database part
        messages.create(FAKE_CHAT_ID, FAKE_DEVICE_UUID, data)

        # Frontend part
        self.event_registry.emit_event('MESSAGE_RECEIVED', data)