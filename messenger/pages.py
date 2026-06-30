from messenger.widgets.debug.chats import DebugChats
from messenger.widgets.debug.devices import DebugDevices
from messenger.widgets.debug.messages import DebugMessages
from messenger.widgets.debug.settings import DebugSettings
from messenger.widgets.debug.advertise import DebugAdvertiser
from messenger.widgets.debug.scanner import DebugBLEScanner
from messenger.widgets.frontend.home import HomeView

DEBUG_PAGES = {
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