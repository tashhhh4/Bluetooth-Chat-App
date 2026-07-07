import logging
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty
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

    chat_id = NumericProperty()
    chat_title = StringProperty()
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
        self.text_input = MDTextField(size_hint_x=.8, )
        self.send_message_form.add_widget(self.text_input)

        # Send Button
        self.send_button = MDButton(style='filled')
        self.send_message_form.add_widget(self.send_button)
        self.send_button_label = MDButtonText(text='Send', size_hint_x=.2)
        self.send_button.add_widget(self.send_button_label)

        ### Bind Actions ###

        # Send Message
        def s(_):
            text = self.text_input.text
            message_service = get_message_service()
            message_service.send_message(text, self.chat_id)
            self._load_messages()
        self.send_button.bind(on_press=s)

    def populate_messages(self, messages):
        logging.info('ChatView: Running populate_messages()')
        def c(_):
            self.message_container.clear_widgets()
        def d(_):
            for message in messages:
                self.message_container.add_widget(MessageCard(message=message))
            self.message_container.add_widget(MDWidget())
        schedule(c)
        schedule(d)

    def set_context(self, **context):
        self.chat_id = context.get('chat_id')
        self.chat_title = context.get('chat_title')

    def on_chat_id(self, _, chat_id):
        logging.info('ChatView: Running on_chat_id')
        self._load_messages()

    def on_chat_title(self, _, chat_title):
        self.headline.text = chat_title

    def on_messages(self, _, messages):
        logging.info('ChatView: Running on_messages()')
        self.populate_messages(messages)

    def _handle_message_received(self):
        logging.info('ChatView: Running _handle_message_received()')
        self._load_messages()

    def _load_messages(self):
        logging.info('ChatView: Running _load_messages()')
        message_service = get_message_service()
        messages = message_service.load_messages(self.chat_id)
        logging.info(f'ChatView: Got {len(messages)} messages from MessageService.')
        self.messages = messages
