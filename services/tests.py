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

    def test_connection_initialized(self):
        connection = Connection(None)
        self.assertIsNone(connection.socket)
        self.assertIsInstance(connection.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        connection = Connection(None)
        connection.socket = {'name': 'Dummy'} # Should emit CONNECTION_ESTABLISHED
        self.assertIn('CONNECTION_ESTABLISHED', self.logs[-1])
        connection.socket = None
        self.assertIn('CONNECTION_LOST', self.logs[-1])

    def test_connection_io_errors(self):
        connection = Connection(None)
        with self.assertRaises(IOError):
            connection.start_reading_input_stream(on_receive=None, on_disconnect=None)
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
        connection._handle_receive('foo')
        self.assertIn('foo', self.logs[-2])
        self.assertIn('MESSAGE_RECEIVED', self.logs[-1])
