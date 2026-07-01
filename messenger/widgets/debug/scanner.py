from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from .components.debug_layout import DebugLayout
from services.platform import get_ble_scanner
from utils import schedule

class DebugBLEScanner(DebugLayout):

    is_scanning = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DebugBLEScanner, self).__init__(**kwargs)

        self.ble = get_ble_scanner()
        self.ble.on_device_discovered = self.display_devices

        self.ble.on_begin_scan = self.start_scanning
        self.ble.on_end_scan = self.stop_scanning
        self.bind(is_scanning=self.update_scan_button)

        self.orientation = 'vertical'
        self.scroll = ScrollView()
        self.devices_container = GridLayout(
            cols=1,
            spacing=dp(4),
            size_hint_y=None,
        )
        self.devices_container.bind(minimum_height=self.devices_container.setter('height'))
        self.scroll.add_widget(self.devices_container)
        self.add_widget(self.scroll)

        self.check_button = Button(
            text='Begin Scan',
            size_hint_y=None,
            height=dp(80)
        )
        self.check_button.bind(on_press=self.on_check_devices_button_pressed)
        self.add_widget(self.check_button)

    def start_scanning(self):
        self.is_scanning = True

    def stop_scanning(self):
        self.is_scanning = False

    def update_scan_button(self, _, value):
        if value is True:
            self.check_button.text = 'Stop Scanning'
        else:
            self.check_button.text = 'Begin Scan'

    def display_devices(self, devices):
        def d(_):
            self.devices_container.clear_widgets()
            for i, device in enumerate(devices):
                self.devices_container.add_widget(Label(
                    text=f'{i + 1}. {device["name"]}\n{device["address"]}',
                    size_hint_y=None,
                    size_hint_x=1,
                    height=dp(200),
                    halign='left',
                    valign='middle',
                ))
        schedule(d)

    def on_check_devices_button_pressed(self, _):
        if self.is_scanning:
            self.ble.stop()
        else:
            self.ble.scan()
