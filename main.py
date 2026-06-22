import config

from android.permissions import request_permissions, Permission
from kivy.app import App
from kivymd.app import MDApp
from messenger.widgets import DebugNavigation, HomeView, RootLayout
from messenger.ui.loader import load_ui
import db.engine as db

DEBUG = True

class Blu2App(MDApp):
    def build(self):

        load_ui()

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

        root_widget = RootLayout()
        root_widget.set_page(HomeView())

        if DEBUG:
            root_widget.add_header(DebugNavigation(root=root_widget))

        return root_widget

Blu2App().run()