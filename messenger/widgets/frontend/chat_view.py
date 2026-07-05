from kivymd.uix.divider import MDDivider

from kivy.metrics import dp
from kivy.properties import DictProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from ..app_screen import AppScreen
from .components.back_link import BackLink

class ChatView(AppScreen):

    device = DictProperty({})

    def __init__(self, **kwargs):

        super(ChatView, self).__init__(**kwargs)

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
        self.headline = MDLabel(text='[loading device info]', font_style='Headline')
        self.headline_container.add_widget(self.headline)

        # Divider
        self.divider = MDDivider()
        self.header.add_widget(self.divider)

    def set_context(self, **context):
        self.device = context.get('device')

    def on_device(self, _, device):
        device_name = device['name'] if device['name'] else 'Unknown Device'
        self.headline.text = f'Chat with {device_name}'