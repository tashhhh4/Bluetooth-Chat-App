""" This module is responsible for wrapping Android-specific operations and providing
    placeholders that allow the app to continue to be tested on the local development PC
    with limited functionality. It provides the appropriate platform-dependant
    initialization behavior for several start-up functions. It instantiates and returns
    singletons of the services classes that encapsulate complicated low-level APIs.
"""

import logging
from kivy.app import App
from config import ENVIRONMENT
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
            window = activity.getWindow()

            # Prevent keyboard from covering up inputs
            window.setSoftInputMode(LayoutParams.SOFT_INPUT_ADJUST_RESIZE)

        schedule(_configure_android_window)

# Todo: Fix the app being drawn underneath the top status bar
def get_top_inset():
    if ENVIRONMENT == 'local':
        return 0
    return 10

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

def run_with_permissions(permissions, callback, on_deny=None):
    """ If all the needed permissions are already granted, immediately run callback().
        Otherwise, initiate a permission request and pass in callback() to be run when done.
        The optional on_deny() handler can be run if the user does not grant the permissions.
    """
    print('Running run_with_permissions()')
    print('The permissions I want to check are', permissions)
    from android.permissions import check_permission, request_permissions
    # if all(check_permission(p) for p in permissions):
    all_granted = True
    for p in permissions:
        print(p, 'is', check_permission(p))
        if not check_permission(p):
            print('Not all permissions were granted.')
            all_granted = False
            break
    if all_granted:
        print('All permissions are already granted.')
        callback()
        return

    def _handle_permission_result(_, grants):
        print('Running run_with_permissions() -> _handle_permission_result()')
        print('permissions:', _, 'grants:', grants)
        if all(grants):
            callback()
        else:
            if on_deny:
                on_deny()

    request_permissions(permissions, _handle_permission_result)

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
    """ Returns the one true instance of MessageService, or a placeholder. """
    existing_obj = App.get_running_app().message_service
    if existing_obj:
        return existing_obj

    bluetooth_service = get_bluetooth_service()

    if ENVIRONMENT == 'local':
        from services.fake_message import FakeMessageService
        return FakeMessageService(bluetooth_service)

    from services.message import MessageService
    message_service = MessageService(bluetooth_service)
    return message_service
