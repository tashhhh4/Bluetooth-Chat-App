from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from .components.debug_layout import DebugLayout
from services import bluetooth

class DebugBluetooth(DebugLayout):

    is_scanning = False

    def __init__(self, **kwargs):
        super(DebugBluetooth, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', spacing=20)
        self.add_widget(self.container)

        # Make Visible Button
        self.make_visible_button = Button(
            text='Turn discoverability on',
            size_hint_x=0.5,
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5},
        )
        self.container.add_widget(self.make_visible_button)

        # Scan Button
        self.scan_button = Button(
            text='Turn scanning on',
            size_hint_x=0.5,
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5},
        )
        self.container.add_widget(self.scan_button)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)


        ### Bind Actions ###

        # Test Turn Discovery On
        def discoverability_on(_):
            bluetooth.turn_discoverability_on()
            print('Activated Android Bluetooth discoverability mode.')
        self.make_visible_button.bind(on_press=discoverability_on)

        # Test Turn Scanning On
        def scanning_on(_):
            bluetooth.turn_scanning_on()
        self.scan_button.bind(on_press=scanning_on)