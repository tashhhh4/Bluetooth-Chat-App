from messenger.widgets.debug.advertise import DebugAdvertiser
from messenger.widgets.debug.devices import DebugDevices
from messenger.widgets.debug.messages import DebugMessages
from messenger.widgets.debug.scanner import DebugBluetooth
from messenger.widgets.debug.settings import DebugSettings

from messenger.widgets.frontend.home import HomeView

DEBUG_PAGES = {
    'BLE Advertising': DebugAdvertiser,
    'BLE Scanning': DebugBluetooth,
    'Devices': DebugDevices,
    'Messages': DebugMessages,
    'Settings': DebugSettings,
}

PAGES = {
    'Home': HomeView,
}