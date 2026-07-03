from kivy.app import App
from messenger.widgets.debug.bluetooth import DebugBluetooth
from messenger.widgets.debug.chats import DebugChats
from messenger.widgets.debug.devices import DebugDevices
from messenger.widgets.debug.messages import DebugMessages
from messenger.widgets.debug.settings import DebugSettings
from messenger.widgets.debug.advertise import DebugAdvertiser
from messenger.widgets.debug.scanner import DebugBLEScanner
from messenger.widgets.frontend.home import HomeView

def change_page(widget, **kwargs):
    app = App.get_running_app()
    app.set_page(widget, **kwargs)

DEBUG_PAGES = {
    'Bluetooth': DebugBluetooth,
    'Devices and Contacts': DebugDevices,
    'Messages': DebugMessages,
    'Chats': DebugChats,
    'Settings': DebugSettings,
    'BLE Advertising': DebugAdvertiser,
    'BLE Scanning': DebugBLEScanner,
}

PAGES = {
    'Home': HomeView,
}