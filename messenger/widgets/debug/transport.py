from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from messenger.widgets.debug.components.debug_layout import DebugLayout
from messenger.widgets.utils import fit_height

# TEMP BACKEND
# Todo: move this stuff out of the frontend
from config import ENVIRONMENT
if ENVIRONMENT == 'debug':
    from pprint import pprint
    import socket
    import jnius
    from jnius import autoclass
    from config import SERVICE_UUID
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    adapter = BluetoothAdapter.getDefaultAdapter()

    def send(address, message):
        pass

    def recv():
        pass


class DebugTransport(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugTransport, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', padding=10, spacing=20)
        self.add_widget(self.container)

        # Page Title
        self.title = Label(text='Transport', font_size=24, size_hint_y=None, height=40)
        self.container.add_widget(self.title)

        # Device UUID
        self.device_info = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        fit_height(self.device_info)
        self.container.add_widget(self.device_info)

        # Label
        self.device_uuid_label = Label(text='Recipient Device UUID', size_hint_y=None, height=30)
        self.device_info.add_widget(self.device_uuid_label)

        # Input
        self.device_uuid_input = TextInput(size_hint_y=None, height=50)
        self.device_info.add_widget(self.device_uuid_input)

        # SEND Button
        self.send_button = Button(
            text='SEND',
            background_color='yellow',
            size_hint_y=None,
            height=50,
            size_hint_x=.6,
            pos_hint={'center_x': .5},
        )
        self.container.add_widget(self.send_button)

        # SEND Button tooltip
        self.send_button_tooltip = Label(text='Sends "Hello World".', font_size=14, size_hint_y=None, height=30)
        self.container.add_widget(self.send_button_tooltip)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)