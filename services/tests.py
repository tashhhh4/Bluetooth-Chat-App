import unittest
from services.bluetooth import BluetoothService
from services.connection import Connection
from utils import EventRegistry

class ServiceTests(unittest.TestCase):

    def test_bluetooth_service_initialized(self):
        bluetooth_service = BluetoothService()
        assert hasattr(bluetooth_service, 'connection')
        assert type(bluetooth_service.connection) is Connection
        assert hasattr(bluetooth_service, 'event_registry')
        assert type(bluetooth_service.event_registry) is EventRegistry
        for event in ['CONNECTION_ESTABLISHED', 'CONNECTION_LOST', 'MESSAGE_RECEIVED']:
            assert event in bluetooth_service.event_registry._callbacks.keys()