from android.permissions import request_permissions, Permission
from kivy.app import App
from messenger.widgets import DebugNavigation, HomeView, RootLayout
import db.engine as db

DEBUG = True

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

        root_widget = RootLayout()
        home_widget = HomeView()

        if DEBUG:
            root_widget.add_header(DebugNavigation(root=root_widget))

        root_widget.set_page(home_widget)

        return root_widget

Blu2App().run()