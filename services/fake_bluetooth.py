import logging
from utils import EventRegistry
from services.connection import Connection

TAG = 'FakeBluetoothService: '
EXPLANATION = ' — not implemented in FakeBluetoothService'

class FakeBluetoothService:

    def __init__(self):
        self.discovered_devices = {}
        self.event_registry = EventRegistry(['DISCOVERED_DEVICES_UPDATED', 'BONDED_DEVICES_UPDATED'])

    @staticmethod
    def scan_for_devices():
        logging.debug(TAG + 'Scan for devices' + EXPLANATION)

    @staticmethod
    def stop_scanning():
        logging.debug(TAG + 'Stop scanning' + EXPLANATION + ' because scan was never started')

    @staticmethod
    def turn_discoverability_on(ttl):
        logging.debug(
                TAG + 'Make this device visible (discoverable) by other Bluetooth' +
                ' devices for ' + str(ttl) + ' seconds' + EXPLANATION
        )

    @staticmethod
    def turn_discovery_on():
        logging.debug(
                TAG + 'Turn discovery mode on using device\'s ' +
                'default Bluetooth adapter' + EXPLANATION
        )

    @staticmethod
    def turn_discovery_off():
        logging.debug(TAG + 'Turn Bluetooth discovery mode off' + EXPLANATION)

    @staticmethod
    def load_paired_devices():
        logging.debug(TAG + 'Get paired Bluetooth devices' + EXPLANATION)
        return []

    @staticmethod
    def listen_for_connections():
        logging.debug(TAG + 'Listen for connections' + EXPLANATION)
