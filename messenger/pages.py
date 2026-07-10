# from messenger.widgets.debug.bluetooth import DebugBluetooth
from messenger.widgets.debug.chat import DebugChat
from messenger.widgets.debug.chats import DebugChats
from messenger.widgets.debug.devices import DebugDevices
from messenger.widgets.debug.messages import DebugMessages
from messenger.widgets.debug.settings import DebugSettings
from messenger.widgets.frontend.bluetooth_manager_view import BluetoothManagerView
from messenger.widgets.frontend.chat_view import ChatView
from messenger.widgets.frontend.chats_view import ChatsView
from messenger.widgets.frontend.home_view import HomeView

DEBUG_PAGES = {
    # 'Bluetooth': DebugBluetooth,
    'Debug Devices': DebugDevices,
    'Debug Messages': DebugMessages,
    'Debug Chats': DebugChats,
    'Debug Settings': DebugSettings,
}

PAGES = {
    'Home': HomeView,
    'Bluetooth Manager': BluetoothManagerView,
    'Chat': ChatView,
    'Chats': ChatsView,
}

VIEWS = {
    'Debug Chat': DebugChat,
}
