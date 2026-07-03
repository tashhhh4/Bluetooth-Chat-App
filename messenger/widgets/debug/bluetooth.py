from kivy.metrics import dp
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from .components.debug_layout import DebugLayout
from services.platform import get_bluetooth_service

SCAN_ON_TEXT = 'Stop scanning'
SCAN_OFF_TEXT = 'Scan'

class DebugBluetooth(DebugLayout):

    is_scanning = BooleanProperty(False)
    bluetooth_service = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DebugBluetooth, self).__init__(**kwargs)

        self.bluetooth_service = get_bluetooth_service()
        self.bluetooth_service.register_event_callback('DEVICE_DISCOVERED', lambda: print('Hello I see you have discovered a device...'))

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', spacing=dp(20))
        self.add_widget(self.container)

        # Make Visible Button
        self.make_visible_button = Button(
            text='Turn discoverability on',
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 0.5},
        )
        self.container.add_widget(self.make_visible_button)

        # Scan Button
        self.scan_button = Button(
            text=SCAN_OFF_TEXT,
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 0.5},
        )
        self.container.add_widget(self.scan_button)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)


        ### Bind Actions ###

        # Test Turn Discovery On
        def discoverability_on(_):
            self.bluetooth_service.turn_discoverability_on(60)
            self.bluetooth_service.listen_for_service_record(60)
        self.make_visible_button.bind(on_press=discoverability_on)

        # Test Turn Scanning On and Off
        def toggle_scanning(_):
            if not self.is_scanning:
                self.bluetooth_service.scan_for_devices()
                self.is_scanning = True
                self.scan_button.text = SCAN_ON_TEXT
            else:
                self.bluetooth_service.stop_scanning()
                self.is_scanning = False
                self.scan_button.text = SCAN_OFF_TEXT

        self.scan_button.bind(on_press=toggle_scanning)

    def populate_available_devices_list(self):
        pass