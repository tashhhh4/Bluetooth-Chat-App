import logging
import unittest
from unittest.mock import patch
from services.bluetooth import BluetoothService
from services.connection import Connection
from services.message import MessageService
from services.platform import ListHandler
from utils import EventRegistry

HIDE_LOGS = True

class PretendSocket:
    def getInputStream(self):
        return None

class ServiceTests(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()

        self.console_handler = next(h for h in logger.handlers if h.__class__.__name__ == 'ConsoleHandler')
        if HIDE_LOGS:
            logger.removeHandler(self.console_handler)

        self.list_in_memory_handler = ListHandler()
        self.list_in_memory_handler.setFormatter(
            logging.Formatter('[TEST] [%(levelname)s] [%(asctime)s] %(message)s')
        )
        logger.addHandler(self.list_in_memory_handler)
        self.logs = self.list_in_memory_handler.logs

    def tearDown(self):
        logger = logging.getLogger()
        logger.removeHandler(self.list_in_memory_handler)
        if HIDE_LOGS:
            logger.addHandler(self.console_handler)

    # Tests

    def test_bluetooth_service_initialized(self):
        bluetooth_service = BluetoothService()
        self.assertHasAttr(bluetooth_service, 'connection')
        self.assertIsInstance(bluetooth_service.connection, Connection)
        self.assertHasAttr(bluetooth_service, 'event_registry')
        self.assertIsInstance(bluetooth_service.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, bluetooth_service.event_registry._callbacks.keys())

    def test_connection_initialized(self):
        connection = Connection(None)
        self.assertIsNone(connection.socket)
        self.assertIsInstance(connection.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        connection = Connection(None)
        connection._handle_disconnect()
        self.assertIn('CONNECTION_LOST', self.logs[-1])

    def test_connection_io_errors(self):
        connection = Connection(None)
        with self.assertRaises(IOError):
            connection._start_reading_input_stream()
        with self.assertRaises(IOError):
            connection.send_bytes('data')

    def test_message_service_initialized(self):
        bluetooth_service = BluetoothService()
        message_service = MessageService(bluetooth_service)
        self.assertHasAttr(message_service, 'connection')
        self.assertIsNone(message_service.connection)
        self.assertIsInstance(message_service.bluetooth_service.connection, Connection)

    def test_bluetooth_service_and_connection_event_timing(self):
        bluetooth_service = BluetoothService()
        connection = bluetooth_service.connection

        # connection receives message, emits event,
        # then bluetooth_service receives message, emits event.
        connection._handle_receive('foo')
        self.assertIn('foo', self.logs[-5])
        self.assertIn('Connection.EventRegistry', self.logs[-4])
        self.assertIn('MESSAGE_RECEIVED', self.logs[-4])
        self.assertIn('foo', self.logs[-2])
        self.assertIn('BluetoothService.EventRegistry', self.logs[-1])
        self.assertIn('MESSAGE_RECEIVED', self.logs[-1])

        # connection emits event after connection._handle_disconnect,
        # then bluetooth_service emits event.
        connection._handle_disconnect()
        self.assertIn('Connection.EventRegistry', self.logs[-2])
        self.assertIn('CONNECTION_LOST', self.logs[-2])
        self.assertIn('BluetoothService.EventRegistry', self.logs[-1])
        self.assertIn('CONNECTION_LOST', self.logs[-1])

        # connection emits event when socket is set to something,
        # then bluetooth_service emits event.
        pretend_socket = PretendSocket()
        with patch.object(connection, '_start_reading_input_stream'):
            bluetooth_service._handle_connection(pretend_socket)
        self.assertIs(connection.socket, pretend_socket)
        self.assertIn('Connection.EventRegistry', self.logs[-2])
        self.assertIn('CONNECTION_ESTABLISHED', self.logs[-2])
        self.assertIn('BluetoothService.EventRegistry', self.logs[-1])
        self.assertIn('CONNECTION_ESTABLISHED', self.logs[-1])

    def test_connection_and_message_service_event_timing(self):
        bluetooth_service = BluetoothService()
        message_service = MessageService(bluetooth_service)

        # connection emits even after disconnect occurs,
        # then message_service emits disconnect event
        message_service.bluetooth_service.connection._handle_disconnect()
        self.assertIn('Connection.EventRegistry', self.logs[-4])
        self.assertIn('CONNECTION_LOST', self.logs[-4])
        self.assertIn('MessageService.EventRegistry', self.logs[-1])
        self.assertIn('DEVICE_DISCONNECTED', self.logs[-1])