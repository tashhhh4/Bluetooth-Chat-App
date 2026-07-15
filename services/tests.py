import unittest
from services.bluetooth import BluetoothService
from services.connection import Connection

class ServiceTests(unittest.TestCase):

    def test_bluetooth_service_contains_connection(self):
        bluetooth_service = BluetoothService()
        assert hasattr(bluetooth_service, 'connection')
        assert type(bluetooth_service.connection) is Connection