import config

from messenger.widgets.debug.devices import DebugDevices
from messenger.widgets.debug.messages import DebugMessages
from messenger.widgets.debug.settings import DebugSettings

from messenger.widgets.frontend.home import HomeView

DEBUG_PAGES = {
    'Devices': DebugDevices,
    'Messages': DebugMessages,
    'Settings': DebugSettings,
}

if config.ENVIRONMENT != 'local':
    from messenger.widgets.debug.advertise import DebugAdvertiser
    from messenger.widgets.debug.scanner import DebugBluetooth
    DEBUG_PAGES['BLE Advertising'] = DebugAdvertiser
    DEBUG_PAGES['BLE Scanning'] = DebugBluetooth


PAGES = {
    'Home': HomeView,
}