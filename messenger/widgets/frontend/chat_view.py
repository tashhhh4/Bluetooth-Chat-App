from kivy.metrics import dp
from kivy.properties import DictProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget
from utils import schedule
from services.platform import get_message_service
from ..app_screen import AppScreen
from .components.back_link import BackLink
from .components.message_card import MessageCard

class ChatView(AppScreen):

    device = DictProperty({})
    messages = ListProperty([])

    def __init__(self, **kwargs):

        message_service = get_message_service()
        message_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)

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

        # Connection Status
        self.connection_hint = MDLabel(
            text='Connected... ?',
            size_hint_y=None,
            height=dp(18),
        )
        self.headline_container.add_widget(self.connection_hint)

        # Divider
        self.divider = MDDivider()
        self.header.add_widget(self.divider)

        # List of Messages
        self.message_container = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.container.add_widget(self.message_container)

        # Message Form
        self.send_message_form = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        self.container.add_widget(self.send_message_form)

        # Text Input
        self.text_input = MDTextField(size_hint_x=.8)
        self.send_message_form.add_widget(self.text_input)

        # Send Button
        self.send_button = MDButton(style='filled')
        self.send_message_form.add_widget(self.send_button)
        self.send_button_label = MDButtonText(text='Send', size_hint_x=.2)
        self.send_button.add_widget(self.send_button_label)

        ### Bind Actions ###

        # Send Message
        def s(_):
            print('Sending message...')
            text = self.text_input.text
            message_service = get_message_service()
            message_service.send_message(text)
            message_from_self = {'text': text, 'sender': 'You', 'time': 'Just now'}
            self.messages.append(message_from_self)
        self.send_button.bind(on_press=s)

    def populate_messages(self, messages):
        def c(_):
            self.message_container.clear_widgets()
        def d(_):
            for message in messages:
                self.message_container.add_widget(MessageCard(message=message))
            self.message_container.add_widget(MDWidget())
        schedule(c)
        schedule(d)

    def set_context(self, **context):
        self.device = context.get('device')

    def on_device(self, _, device):
        device_name = device['name'] if device['name'] else 'Unknown Device'
        self.headline.text = f'Chat with {device_name}'

    def on_messages(self, _, messages):
        self.populate_messages(messages)

    def _handle_message_received(self, data):
        message = {'text': data, 'sender': self.device['name'], 'time': 'Just now'}
        self.messages.append(message)