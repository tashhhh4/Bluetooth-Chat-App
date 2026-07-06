from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from services.platform import get_bluetooth_service
from messenger.utils import change_page

def connect_to_device(device):
    print('Connecting to device...')
    bluetooth_service = get_bluetooth_service()
    bluetooth_service.connect_to_device(device['address'])

class DeviceCard(MDCard):
    def __init__(self, device, **kwargs):

        self.device = device

        super(DeviceCard, self).__init__(**kwargs)

        # Top-level Container
        self.container = MDBoxLayout(orientation='horizontal')
        self.add_widget(self.container)

        # Device Info -- Left Column
        self.device_info = MDBoxLayout(orientation='vertical', size_hint_x=.7)
        self.container.add_widget(self.device_info)

        # Device Name and Address
        self.device_info.add_widget(MDLabel(text=str(device['name']), halign='left'))
        self.device_info.add_widget(MDLabel(text=device['address'], halign='left'))

        # Connect Button Container -- Right Column
        self.button_container = MDBoxLayout(size_hint_x=.3)
        self.container.add_widget(self.button_container)

        # Connect Button
        self.button = MDButton(
            size_hint_y=None,
            size_hint_x=None,
            width=dp(100),
            height=dp(40),
            pos_hint={'x_center': 0.5},
        )
        self.button_container.add_widget(self.button)
        self.button_text = MDButtonText(text='Connect')
        self.button.add_widget(self.button_text)

        ### Bind Actions ###

        def c(_):
            connect_to_device(self.device)
        self.button.bind(on_press=c)