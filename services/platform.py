""" This module is responsible for choosing the correct version of a Service
    and instantiating singletons. A Service is a class that encapsulates
    complicated low-level APIs such as Bluetooth and and Android Permissions.
"""

from kivy.app import App
from config import ENVIRONMENT, RUN_TESTS
from utils import schedule
from services.connection import Connection

def configure_desktop_window():
    from kivy.config import Config
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '740')

def run_tests():
    if RUN_TESTS is True:
        import unittest
        from pathlib import Path
        project_root = Path(__file__).resolve().parent.parent
        loader = unittest.TestLoader()
        if ENVIRONMENT == 'debug':
            naming_scheme = 'test*android.py'
        elif ENVIRONMENT == 'local':
            naming_scheme = 'test*desktop.py'
        else:
            naming_scheme = 'test*.py'
        suite = loader.discover(start_dir=str(project_root), pattern=naming_scheme)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)

def configure_android_window():
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

def configure_window():
    if ENVIRONMENT == 'local':
        configure_desktop_window()

    else:
        configure_android_window()

# Todo: Fix the app being drawn underneath the top status bar
def get_top_inset():
    if ENVIRONMENT == 'local':
        return 0
    return 10

def get_bluetooth_service():
    """ Returns the BluetoothService class for Android or Desktop,
        or a placeholder implementing dummy methods.
    """
    existing_obj = App.get_running_app().bluetooth_service
    if existing_obj:
        return existing_obj

    if ENVIRONMENT == 'local':
        from services.bluetooth_desktop import DesktopBluetoothService
        return DesktopBluetoothService()

    elif ENVIRONMENT == 'debug':
        from services.bluetooth_android import AndroidBluetoothService
        return AndroidBluetoothService()

    from services.bluetooth_fake import FakeBluetoothService
    return FakeBluetoothService()

def get_connection():
    """ Returns a Connection() which uses the BluetoothService as its backbone,
        but may not necessarily be a singleton.
    """
    bluetooth_service = get_bluetooth_service()
    return Connection(bluetooth_service)

def get_message_service():
    """ Returns the one true instance of `services.message.MessageService`,
        or a placeholder.
    """
    existing_obj = App.get_running_app().message_service
    if existing_obj:
        return existing_obj

    connection = get_connection()

    if ENVIRONMENT == 'local':
        from services.fake_message import FakeMessageService
        return FakeMessageService(connection)

    from services.message import MessageService
    message_service = MessageService(connection)
    return message_service
