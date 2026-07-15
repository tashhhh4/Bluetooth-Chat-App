""" This module is responsible for choosing the correct version of a Service
    and instantiating singletons. A Service is a class that encapsulates
    complicated low-level APIs such as Bluetooth and and Android Permissions.
"""

from kivy.app import App
from config import ENVIRONMENT, RUN_TESTS
from utils import schedule

def configure_desktop_window():
    from kivy.config import Config
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '740')

def run_tests():
    if ENVIRONMENT == 'debug' and RUN_TESTS is True:
        import unittest
        from pathlib import Path
        project_root = Path(__file__).resolve().parent.parent
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=str(project_root), pattern='test*.py')
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
    """ Returns the one true instance of `services.bluetooth.BluetoothService,
        or a placeholder.
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
    """ Returns the one true instance of `services.message.MessageService`,
        or a placeholder.
    """
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
