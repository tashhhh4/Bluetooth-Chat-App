from kivy.properties import ListProperty
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import MDWidget
from services.platform import get_bluetooth_service
from utils import schedule
from ..app_screen import AppScreen
from .components.back_link import BackLink
from .components.device_card import DeviceCard

class BluetoothManagerView(AppScreen):

    paired_devices = ListProperty([])

    def __init__(self, **kwargs):

        self.bluetooth_service = get_bluetooth_service()
        self.bluetooth_service.event_registry.register_event_callback('BONDED_DEVICES_UPDATED', self._handle_bonded_devices_updated)

        super(BluetoothManagerView, self).__init__(**kwargs)

        # Top-level Container
        self.container = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(20))
        self.add_widget(self.container)

        # Header
        self.header = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(40))
        self.container.add_widget(self.header)

        # Headline Container
        self.headline_container = MDBoxLayout(orientation='horizontal')
        self.header.add_widget(self.headline_container)

        # Back Link
        self.back_link = BackLink('Home', icon='arrow-left')
        self.headline_container.add_widget(self.back_link)

        # Headline
        self.headline = MDLabel(text='Bluetooth Connections', font_style='Headline')
        self.headline_container.add_widget(self.headline)

        # Divider
        self.divider = MDDivider()
        self.header.add_widget(self.divider)

        # Make Visible Section Card - DISABLED
        self.make_visible_section = MDCard(style='elevated', size_hint_y=None, height=dp(80))
        # self.container.add_widget(self.make_visible_section)

        # Make Visible Section Layout - DELETE PARENT COMMENT-OUT TO REENABLE
        self.make_visible_layout = MDBoxLayout(orientation='horizontal', padding=dp(10), spacing=dp(20))
        self.make_visible_section.add_widget(self.make_visible_layout)

        # Make Visible Section Caption - DELETE PARENT COMMENT-OUT TO REENABLE
        self.make_visible_caption = MDLabel(
            text='Click here to make your device discoverable to other devices using Bluetooth.',
            font_style='Label',
            size_hint_x=.5,
        )
        self.make_visible_layout.add_widget(self.make_visible_caption)

        # Make Visible Section Button
        self.make_visible_button = MDButton(style='filled', size_hint_x=.3)
        self.make_visible_layout.add_widget(self.make_visible_button)
        self.make_visible_button_text = MDButtonText(text='Make Visible')
        self.make_visible_button.add_widget(self.make_visible_button_text)

        # Paired Devices
        self.paired_devices_section = MDBoxLayout(orientation='vertical')
        self.container.add_widget(self.paired_devices_section)

        # Paired Devices Title
        self.paired_devices_title = MDLabel(text='Paired Devices', font_style='Title', size_hint_y=None, height=dp(30))
        self.paired_devices_section.add_widget(self.paired_devices_title)

        # Paired Devices Container
        self.paired_devices_container = MDBoxLayout(orientation='vertical')
        self.paired_devices_section.add_widget(self.paired_devices_container)

        self.load_paired_devices()

    def populate_paired_devices_list(self, devices):
        paired_devices_list = self.paired_devices_container

        def c(_):
            paired_devices_list.clear_widgets()
        def d(_):
            for device in devices:
                device_card = DeviceCard(device)
                paired_devices_list.add_widget(device_card)

            spacer = MDWidget()
            paired_devices_list.add_widget(spacer)

        schedule(c)
        schedule(d)

    def load_paired_devices(self):
        self.bluetooth_service.load_paired_devices()

    def on_paired_devices(self, _, devices):
        self.populate_paired_devices_list(devices)

    def _handle_bonded_devices_updated(self, devices):
        self.paired_devices = devices
