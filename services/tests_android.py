from unittest.mock import patch
from services.android import AndroidService
from services.bluetooth_android import AndroidBluetoothService
from services.connection import Connection
from services.message import MessageService, MessageObject, Message
from utils import EventRegistry, TestSuite

class PretendSocket:
    def getInputStream(self):
        return None

class ServiceTests(TestSuite):

    def test_android_service_initialized(self):
        android_service = AndroidService()
        self.assertHasAttr(android_service, 'event_registry')
        self.assertEqual(android_service.event_registry.name, 'AndroidService.EventRegistry')

    def test_bluetooth_service_initialized(self):
        bluetooth_service = AndroidBluetoothService()
        self.assertHasAttr(bluetooth_service, 'event_registry')
        self.assertIsInstance(bluetooth_service.event_registry, EventRegistry)
        self.assertEqual(bluetooth_service.event_registry.name, 'AndroidBluetoothService.EventRegistry')
        for event in ['BONDED_DEVICES_UPDATED', 'CONNECTION_ESTABLISHED', 'DISCOVERED_DEVICES_UPDATED']:
            self.assertIn(event, bluetooth_service.event_registry._callbacks.keys())

    def test_connection_initialized(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)
        self.assertIsNone(connection.socket)
        self.assertEqual(connection.event_registry.name, 'Connection.EventRegistry')
        self.assertIsInstance(connection.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)
        connection._handle_disconnect()
        self.assertIn('CONNECTION_LOST', self.logs[-1])

    def test_connection_io_errors(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)
        with self.assertRaises(IOError):
            connection._start_reading_input_stream()
        with self.assertRaises(IOError):
            connection.send_bytes('data')

    def test_message_service_initialized(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)
        message_service = MessageService(connection)
        self.assertHasAttr(message_service, 'connection')
        self.assertIsInstance(message_service.connection, Connection)

    def test_bluetooth_service_and_connection_event_timing(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)

        # bluetooth_service passes a socket into its _handle_connection,
        # connection emits event,
        # then bluetooth_service emits event.
        pretend_socket = PretendSocket()
        with patch.object(connection, '_start_reading_input_stream'):
            bluetooth_service._handle_connection(pretend_socket)
        self.assertIs(connection.socket, pretend_socket)
        self.assertLogComesAfter(
            ('BluetoothService.EventRegistry', 'CONNECTION_ESTABLISHED'),
            ('Connection.EventRegistry', 'CONNECTION_ESTABLISHED'),
        )

    def test_connection_and_message_service_event_timing(self):
        bluetooth_service = AndroidBluetoothService()
        connection = Connection(bluetooth_service)
        MessageService(connection)

        # connection emits after disconnect occurs,
        # then message_service emits disconnect event
        connection._handle_disconnect()
        self.assertLogComesAfter(
            ('Connection.EventRegistry', 'CONNECTION_LOST'),
            ('MessageService.EventRegistry', 'DEVICE_DISCONNECTED'),
        )

        # connection emits MESSAGE_RECEIVED,
        # then message_service emits MESSAGE_RECEIVED
        message = MessageObject(Message('test'), sender_uuid='12345', role='message')
        data = message.to_json()
        try:
            connection._handle_receive(data)
        except RuntimeError:
            pass
        self.assertLogsInOrder(
            ('Connection', 'Received', 'test'),
            ('Connection.EventRegistry', 'MESSAGE_RECEIVED'),
            ('MessageService', '_handle_message_received')
        )
