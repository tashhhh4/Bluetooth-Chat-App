""" This module is responsible for separating out imports that will cause the app
    to crash when a library isn't available due to being run on Android vs. PC.
    It also instantiates and returns singletons of BluetoothService and MessageService.
    It contains additional initialization functions that run on app startup.
"""

import logging
from kivy.app import App
from config import ENVIRONMENT
from services.message import MessageService
from utils import device_java_obj_to_dict, schedule
from messenger.utils import change_page

"""
Wraps Android-specific operations and provides fallbacks for testing.
"""

from utils import schedule

def initialize_window():
    if ENVIRONMENT == 'local':
        from kivy.config import Config
        Config.set('graphics', 'width', '360')
        Config.set('graphics', 'height', '740')

    else:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        LayoutParams = autoclass('android.view.WindowManager$LayoutParams')

        @run_on_ui_thread
        def _configure_android_window(_):
            activity = PythonActivity.mActivity
            activity.getWindow().setSoftInputMode(LayoutParams.SOFT_INPUT_ADJUST_RESIZE)

        schedule(_configure_android_window)

        # Todo: Fix the app being drawn underneath the top status bar


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
    """ Returns a class that implements all the methods of `/services/bluetooth_discovery.py`,
        but it may work differently depending on the environment.
    """
    if ENVIRONMENT == 'local':
        from services.fake_bluetooth_discovery import FakeBLEScanner
        return FakeBLEScanner()

    from services.bluetooth_discovery import BLEScanner
    return BLEScanner()

def get_bluetooth_service():
    """ Returns an instance of `services.bluetooth.BluetoothService,
        or a fake placeholder class.
    """
    existing_obj = App.get_running_app().bluetooth_service
    if existing_obj:
        return existing_obj

    if ENVIRONMENT == 'local':
        from services.fake_bluetooth import FakeBluetoothService
        return FakeBluetoothService()

    from services.bluetooth import BluetoothService
    bluetooth_service = BluetoothService()
    return bluetooth_service

def get_message_service():
    """ Returns the one true instance of MessageService. """
    existing_obj = App.get_running_app().message_service
    if existing_obj:
        return existing_obj

    bluetooth_service = get_bluetooth_service()
    message_service = MessageService(bluetooth_service)
    return message_service

def get_transport():
    """ Returns something (a class) that can be used to initiate send() and recv(),
        or a fake class allowing the code to continue to be debugged on desktop.
    """