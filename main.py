from android.permissions import request_permissions, Permission
from kivy.app import App
from messenger.widgets import DebugBluetoothDevices
import db.engine as db

class Blu2App(App):
    def build(self):

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

        db.initialize_database()
        return DebugBluetoothDevices()

Blu2App().run()