from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from services.bluetooth import BLE

class DebugBluetoothDevices(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugBluetoothDevices, self).__init__(**kwargs)

        self.ble = BLE()

        self.orientation = 'vertical'
        self.scroll = ScrollView()
        self.devices_container = GridLayout(
            cols=1,
            spacing=4,
            size_hint_y=None,
        )
        self.devices_container.bind(minimum_height=self.devices_container.setter('height'))
        self.scroll.add_widget(self.devices_container)
        self.add_widget(self.scroll)

        self.check_button = Button(
            text='Refresh Device List',
            size_hint_y=None,
            height=80
        )
        self.check_button.bind(on_press=self.on_check_devices_button_pressed)
        self.add_widget(self.check_button)

    def update_devices(self, devices): # temp placeholder
        self.devices_container.clear_widgets()
        for device in devices:
            self.devices_container.add_widget(Label(
                text=device,
                size_hint_y=None,
                halign='left',
                valign='middle',
                text_size=(280, None),
            ))

    def on_check_devices_button_pressed(self, button_instance):
        self.ble.scan()
        print('Starting BLE scan.')
        self.update_devices(['Device 1', 'Device 2', 'Device 3'])