import socket
from kivy.app import App
import db.engine as db
from messenger.widgets import DebugMessages

MY_BLUETOOTH_ADAPTER_MAC_ADDRESS = 'd0:39:57:9d:5f:78'

class Blu2App(App):
    def build(self):
        db.initialize_database()

        print('\n\n\n\n')
        print('RUNNING BUILD')
        print('-------------')
        print('Excalibux Bluetooth MAC address:', MY_BLUETOOTH_ADAPTER_MAC_ADDRESS)
        print('socket has AF_BLUETOOTH:', hasattr(socket, 'AF_BLUETOOTH'))

        # Attempt to send a client connection
        client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        print("Created client:", client, type(client))
        print('\n\n\n\n')

        return DebugMessages()

Blu2App().run()