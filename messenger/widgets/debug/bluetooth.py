from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from utils import schedule
from .components.debug_layout import DebugLayout
from ..utils import add_background, fit_height
from messenger.utils import change_page
from services.platform import get_bluetooth_service

SCAN_ON_TEXT = 'Stop scanning'
SCAN_OFF_TEXT = 'Scan'

def open_chat_with_device(device):
    print('Opening a new chat.')
    print('Running open_chat_with_device.')
    bluetooth_service = get_bluetooth_service()
    bluetooth_service.connect_to_device(device['address'])
    print('Before calling change_page')
    change_page('Debug Chat', device=device)
    print('After calling change_page')

class DeviceCard(BoxLayout):
    def __init__(self, device, card_color=(.1, .1, .1, 1.), **kwargs):
        super(DeviceCard, self).__init__(**kwargs)

        self.size_hint_y = None
        self.height = dp(40)

        # Top-Level Container
        self.container = BoxLayout(orientation='horizontal')
        add_background(self.container, card_color)
        self.add_widget(self.container)

        # Device Info -- Left Column
        self.device_info = BoxLayout(orientation='vertical', size_hint_x=.7)
        self.container.add_widget(self.device_info)

        # Device Name and Address
        self.device_info.add_widget(Label(text=str(device['name']), halign='left'))
        self.device_info.add_widget(Label(text=str(device['address']), halign='left'))

        # Connect Button Container -- Right Column
        self.button_container = BoxLayout(size_hint_x=.3)
        self.container.add_widget(self.button_container)

        # Connect Button
        self.button = Button(
            text='Connect',
            size_hint_y=None,
            size_hint_x=None,
            width=dp(100),
            height=dp(40),
            pos_hint={'x_center': 0.5}
        )
        self.button_container.add_widget(self.button)

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
        self.paired_devices_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(5),
        )
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
        self.paired_devices_list = BoxLayout(orientation='vertical', size_hint_y=None)
        fit_height(self.paired_devices_container)
        self.paired_devices_container.add_widget(self.paired_devices_list)
        self.populate_paired_devices_list()

        # Available Devices
        self.available_devices_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(5)
        )
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

        self.bluetooth_service.event_registry.register_event_callback(
            'DISCOVERED_DEVICES_UPDATED',
            self.populate_available_devices_list
        )

    def populate_paired_devices_list(self):
        devices = self.bluetooth_service.get_paired_devices()
        for device in devices:
            # Card
            card = DeviceCard(device, card_color=(.15, .15, .35, 1))
            self.paired_devices_container.add_widget(card)

            # Connect Button Action
            def f(_, dev=device): open_chat_with_device(dev)
            card.button.bind(on_press=f)

    def populate_available_devices_list(self, devices):
        def c(_):
            self.available_devices_container.clear_widgets()
        def d(_):
            for device in devices:
                # Card
                card = DeviceCard(device, card_color=(.2, .2, .2, 1))
                self.available_devices_container.add_widget(card)

                # Connect Button Action
                def f(_, dev=device): open_chat_with_device(dev)
                card.button.bind(on_press=f)

        schedule(c)
        schedule(d)