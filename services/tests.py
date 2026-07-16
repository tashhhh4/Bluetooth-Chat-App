import logging
import unittest
from services.bluetooth import BluetoothService
from services.connection import Connection
from services.platform import ListHandler
from utils import EventRegistry

class ServiceTests(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()

        self.console_handler = next(h for h in logger.handlers if h.__class__.__name__ == 'ConsoleHandler')
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
        logger.addHandler(self.console_handler)

    # Tests

    def test_connection_initialized(self):
        connection = Connection(None, BluetoothService())
        self.assertIsNone(connection.socket)
        self.assertIsInstance(connection.event_registry, EventRegistry)
        self.assertIsInstance(connection.bluetooth_service, BluetoothService)
        self.assertIsInstance(connection.bluetooth_service.connection, Connection)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        bluetooth_service = BluetoothService()
        connection = bluetooth_service.connection
        connection.socket = {'name': 'Dummy'} # Should emit CONNECTION_ESTABLISHED
        self.assertIn('CONNECTION_ESTABLISHED', self.logs[-1])
        connection.socket = None
        self.assertIn('CONNECTION_LOST', self.logs[-1])

    def test_connection_io_errors(self):
        bluetooth_service = BluetoothService()
        connection = bluetooth_service.connection
        with self.assertRaises(IOError):
            connection._start_reading_input_stream()
        with self.assertRaises(IOError):
            connection.send_bytes('data')

    def test_bluetooth_service_initialized(self):
        bluetooth_service = BluetoothService()
        self.assertHasAttr(bluetooth_service, 'connection')
        self.assertIsInstance(bluetooth_service.connection, Connection)
        self.assertHasAttr(bluetooth_service, 'event_registry')
        self.assertIsInstance(bluetooth_service.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, bluetooth_service.event_registry._callbacks.keys())

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

        # connection emits event after socket is set to None,
        # then bluetooth_service emits event.
        connection.socket = None
        self.assertIn('Connection.EventRegistry', self.logs[-2])
        self.assertIn('CONNECTION_LOST', self.logs[-2])
        self.assertIn('BluetoothService.EventRegistry', self.logs[-1])
        self.assertIn('CONNECTION_LOST', self.logs[-1])

        # connection emits event when socket is set to something,
        # then bluetooth_service emits event.
        pretend_socket = {'name': 'Pretend Socket'}
        with self.assertRaises(AttributeError):  # on pretend_socket.getInputStream()
            bluetooth_service._handle_connection(pretend_socket)
        self.assertIs(connection.socket, pretend_socket)
        self.assertIn('BluetoothService.EventRegistry', self.logs[-2])
        self.assertIn('CONNECTION_LOST', self.logs[-2])
        self.assertIn('Connection.EventRegistry', self.logs[-1])
        self.assertIn('CONNECTION_LOST', self.logs[-1])