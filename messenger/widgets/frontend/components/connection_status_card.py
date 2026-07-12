from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from messenger.widgets.utils import (
    bind_height_to_content_height,
    bind_height_to_texture_height,
    wrap_text,
)
from services.platform import get_bluetooth_service

def connect_to_device(device):
    print('[ConnectionStatusCard.connect_to_device]', device)
    bluetooth_service = get_bluetooth_service()
    bluetooth_service.connect_to_device(device.address)

class ConnectionStatusCard(MDCard):

    peer_device = ObjectProperty()

    def __init__(self, blue_text, black_text, peer_device, **kwargs):

        super(ConnectionStatusCard, self).__init__(**kwargs)

        self.style = 'outlined'
        self.padding = dp(10)
        bind_height_to_content_height(self)

        # Vertical Layout
        self.layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.layout)
        self.add_widget(self.layout)

        # Line 1
        self.line_1 = MDBoxLayout(size_hint_y=None, height=dp(40))
        self.layout.add_widget(self.line_1)

        # Blue Text
        self.blue_text = MDLabel(text=f'[b]{blue_text}[/b]', theme_text_color='Custom', text_color=(0, 0, 1, 1), markup=True)
        wrap_text(self.blue_text)
        bind_height_to_texture_height(self.blue_text)
        self.line_1.add_widget(self.blue_text)

        # Connect Button
        self.connect_button = MDButton(style='elevated', theme_width='Custom', width=dp(100), size_hint_x=None)
        self.line_1.add_widget(self.connect_button)

        # Connect Button Text
        self.connect_button_text = MDButtonText(text='Connect')
        self.connect_button.add_widget(self.connect_button_text)

        # Line 2 with Black Text
        self.black_text = MDLabel(text=black_text)
        wrap_text(self.black_text)
        bind_height_to_texture_height(self.black_text)
        self.layout.add_widget(self.black_text)

        #### Bind Action ####

        self.connect_button.bind(on_press=lambda _: connect_to_device(peer_device))
