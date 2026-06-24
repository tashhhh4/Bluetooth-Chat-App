import logging
from config import ENVIRONMENT

"""
Wraps Android-specific operations and provides fallbacks for testing.
"""

def initialize_window():
    if ENVIRONMENT == 'local':
        from kivy.config import Config
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '740')


def initialize_permissions():
    """ Runs request_permissions() if running on Android, else does nothing. """
    if ENVIRONMENT != 'local':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.BLUETOOTH,
            Permission.BLUETOOTH_ADMIN,
            Permission.BLUETOOTH_ADVERTISE,
            Permission.BLUETOOTH_CONNECT,
            Permission.BLUETOOTH_SCAN,
            Permission.ACCESS_BACKGROUND_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.ACCESS_FINE_LOCATION,
        ])
    else:
        logging.info('Skipped requesting Android permissions.')


def get_ble_scanner():
    """ Returns a class that implements all the methods of `/services/blueetooth_discovery.py`,
        but it may work differently depending on the environment.
    """
    if ENVIRONMENT == 'local':
        from services.fake_bluetooth_discovery import FakeBLEScanner
        return FakeBLEScanner()

    from services.bluetooth_discovery import BLEScanner
    return BLEScanner()

def get_transport():
    """ Returns something (a class) that can be used to initiate send() and recv(),
        or a fake class allowing the code to continue to be debugged on desktop.
    """