from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from utils import schedule
from .components.debug_layout import DebugLayout
from ..utils import add_background, fit_height
from services.platform import get_bluetooth_service

SCAN_ON_TEXT = 'Stop scanning'
SCAN_OFF_TEXT = 'Scan'

class DebugBluetooth(DebugLayout):

    is_scanning = BooleanProperty(False)
    bluetooth_service = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DebugBluetooth, self).__init__(**kwargs)

        self.bluetooth_service = get_bluetooth_service()

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

        # Paired Devices
        self.paired_devices_container = BoxLayout(orientation='vertical', size_hint_y=None)
        fit_height(self.paired_devices_container)
        self.container.add_widget(self.paired_devices_container)

        # Heading
        self.paired_devices_label = Label(
            text='Paired Devices',
            size_hint_y=None,
            height=dp(20),
            font_size=sp(12),
            halign='left',
        )
        self.paired_devices_container.add_widget(self.paired_devices_label)

        # List
        self.paired_devices_list = GridLayout(
            cols=1,
            size_hint_y=None,
            row_default_height=dp(40),
            row_force_default=True,
        )
        fit_height(self.paired_devices_container)
        self.paired_devices_container.add_widget(self.paired_devices_list)

        # Available Devices
        self.available_devices_container = BoxLayout(orientation='vertical', size_hint_y=None)
        fit_height(self.available_devices_container)
        self.container.add_widget(self.available_devices_container)

        # Heading
        self.available_devices_label = Label(
            text='Available Devices',
            size_hint_y=None,
            height=dp(20),
            font_size=sp(12),
            halign='left',
        )
        self.available_devices_container.add_widget(self.available_devices_label)

        # List
        self.available_devices_list = BoxLayout(orientation='vertical', size_hint_y=None)
        fit_height(self.available_devices_list)
        self.available_devices_container.add_widget(self.available_devices_list)

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

        ### Bind Events ###

        self.bluetooth_service.register_event_callback(
            'DISCOVERED_DEVICES_UPDATED',
            self.populate_available_devices_list
        )

    def populate_available_devices_list(self, devices):
        print('running populate_available_devices_list')
        self.available_devices_container.clear_widgets()
        print('devices are')
        def d(_):
            print('Going through list.')
            for device in devices:
                print('device is', device)
                # Card
                card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(40))
                add_background(card, (.2, .2, .2, 1))
                self.available_devices_container.add_widget(card)

                # Device Name
                card.add_widget(Label(text=str(device['name'])))
                card.add_widget(Label(text=str(device['address'])))
        schedule(d)