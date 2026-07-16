import logging
import unittest
from services.bluetooth import BluetoothService
from services.connection import Connection
from services.platform import ListHandler
from utils import EventRegistry

class ServiceTests(unittest.TestCase):

    def setUp(self):
        self.list_in_memory_handler = ListHandler()
        self.list_in_memory_handler.setFormatter(
            logging.Formatter('[TEST] [%(levelname)s] [%(asctime)s] %(message)s')
        )
        logging.getLogger().addHandler(self.list_in_memory_handler)

    def tearDown(self):
        logging.getLogger().removeHandler(self.list_in_memory_handler)

    def test_connection_initialized(self):
        connection = Connection(None)
        self.assertIsNone(connection.socket)
        self.assertIsInstance(connection.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, connection.event_registry._callbacks.keys())

    def test_connection_events(self):
        connection = Connection(None)
        connection.socket = {'name': 'Dummy'} # Should emit CONNECTION_ESTABLISHED
        self.assertIn('CONNECTION_ESTABLISHED', self.list_in_memory_handler.logs[-1])


    def test_bluetooth_service_initialized(self):
        bluetooth_service = BluetoothService()
        self.assertHasAttr(bluetooth_service, 'connection')
        self.assertIsInstance(bluetooth_service.connection, Connection)
        self.assertHasAttr(bluetooth_service, 'event_registry')
        self.assertIsInstance(bluetooth_service.event_registry, EventRegistry)
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            self.assertIn(event, bluetooth_service.event_registry._callbacks.keys())
