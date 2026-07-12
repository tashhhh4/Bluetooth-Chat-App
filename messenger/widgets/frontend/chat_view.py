import logging
from kivy.metrics import dp
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty
)
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget
from utils import schedule
from services.platform import get_message_service
from messenger.widgets.utils import (
    bind_height_to_content_height,
    bind_height_to_texture_height,
    wrap_text,
)
from ..app_screen import AppScreen
from .components.message_card import MessageCard
from .components.screen_container import ScreenContainer
from .components.screen_header import ScreenHeader

from .components.button_link import ButtonLink

class ChatView(AppScreen):

    chat_id = NumericProperty()
    chat_title = StringProperty()
    peer_device = ObjectProperty()
    messages = ListProperty([])

    def __init__(self, **kwargs):

        self.connected = False

        message_service = get_message_service()
        message_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)
        message_service.event_registry.register_event_callback('DEVICE_CONNECTED', self._handle_device_connected)
        message_service.event_registry.register_event_callback('DEVICE_DISCONNECTED', self._handle_device_disconnected)

        super(ChatView, self).__init__(**kwargs)

        # Top-level Container
        self.container = ScreenContainer()
        self.add_widget(self.container)

        # Header
        self.header = ScreenHeader(subtitle='Connected... ?', back_link=True, back_loc='Home')
        self.container.add_widget(self.header)

        # Anchor Point for Connection Status Box
        self.connection_status_container = MDBoxLayout()
        bind_height_to_content_height(self.connection_status_container)
        self.container.add_widget(self.connection_status_container)

        # Optionally Visible Connection Status Box
        self.connection_status_box = MDCard(style='outlined')
        bind_height_to_content_height(self.connection_status_box)

        # 2-Line Vertical Layout
        self.connection_status_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.connection_status_layout)
        self.connection_status_box.add_widget(self.connection_status_layout)

        # Line 1 with Blue Text
        self.connection_status_line_1 = MDBoxLayout()
        self.connection_status_layout.add_widget(self.connection_status_line_1)
        self.connection_status_blue_text = MDLabel(text='primary blue')
        wrap_text(self.connection_status_blue_text)
        bind_height_to_texture_height(self.connection_status_blue_text)
        self.connection_status_line_1.add_widget(self.connection_status_blue_text)

        # Connect Button
        # self.connect_button_container = MDBoxLayout()

        # self.connect_button_layout = MDAnchorLayout(anchor_x='center')
        # self.connect_button_container.add_widget(self.connect_button_layout)

        self.connect_button = MDButton(style='elevated', theme_width='Custom', width=dp(300), size_hint_x=None)
        self.container.add_widget(self.connect_button)

        self.connect_button_text = MDButtonText(text='Connect', font_style='Title')
        self.connect_button.add_widget(self.connect_button_text)

        # Line 2 with Black Text
        self.connection_status_line_2 = MDLabel(text='some longer and more detailed explanation in black text')
        wrap_text(self.connection_status_line_2)
        bind_height_to_texture_height(self.connection_status_line_2)
        self.connection_status_layout.add_widget(self.connection_status_line_2)

        # Scroll View
        self.scroll_view = MDScrollView()
        self.container.add_widget(self.scroll_view)

        # List of Messages
        self.message_container = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            padding=dp(10),
            spacing=dp(10)
        )
        self.scroll_view.add_widget(self.message_container)

        # Message Form
        self.send_message_form = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(42), spacing=dp(5))
        self.container.add_widget(self.send_message_form)

        # Text Input
        self.text_input = MDTextField(size_hint_y=1)
        self.send_message_form.add_widget(self.text_input)

        # Send Button
        self.send_button = MDIconButton(style='filled', icon='send')
        self.send_message_form.add_widget(self.send_button)

        ### Bind Actions ###

        # Send Message
        def s(_):
            logging.info('ChatView: Running Send Button function.')
            self.check_connection()
            if not self.connected:
                return

            text = self.text_input.text
            message_service = get_message_service()
            message_service.send_message(text, self.chat_id)
            self.text_input.text = ''
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

    def check_connection(self):
        """ Checks the connection status and if the Connected Device matches the
            one this Chat is designated for.
            Updates the connection status and connection options in the UI accordingly.
        """
        logging.debug('ChatView: Polling MessageService for connection status.')
        message_service = get_message_service()
        if message_service.connected_state == 'CONNECTED':
            device = message_service.connected_device
            if device:
                logging.debug(f'ChatView: Connected with {device.__repr__()}')
                logging.debug(f'ChatView: My Peer device is {self.peer_device.__repr__()}')
                if device == self.peer_device:
                    self.connected = True
                    self.header.subtitle = 'Connected'
                    self.connection_status_container.remove_widget(self.connection_status_box)
                else:
                    logging.debug(f'ChatView: Sorry, but your connected Device is in another Chat.')
                    self.connected = False
                    self.header.subtitle = None
                    self.connection_status_container.add_widget(self.connection_status_box)
        else:
            self.connected = False
            self.header.subtitle = None
            self.connection_status_container.add_widget(self.connection_status_box)

    def set_context(self, **context):
        self.chat_id = context.get('chat_id')
        self.chat_title = context.get('chat_title')
        self.peer_device = context.get('peer_device')

    def on_chat_id(self, _, chat_id):
        logging.info('ChatView: Running on_chat_id')
        self._load_messages()

    def on_chat_title(self, _, chat_title):
        self.header.title = chat_title

    def on_peer_device(self, _, value):
        self.check_connection()

    def on_messages(self, _, messages):
        logging.info('ChatView: Running on_messages()')
        self.populate_messages(messages)

    def on_pre_enter(self):
        if self.chat_id:
            self._load_messages()
        if self.peer_device:
            self.check_connection()

    def _load_messages(self):
        logging.info('ChatView: Running _load_messages()')
        message_service = get_message_service()
        messages = message_service.load_messages(self.chat_id)
        logging.info(f'ChatView: Got {len(messages)} messages from MessageService.')
        self.messages = messages

    def _handle_message_received(self):
        logging.info('ChatView: Running _handle_message_received()')
        self._load_messages()

    def _handle_device_connected(self):
        self.check_connection()

    def _handle_device_disconnected(self):
        self.check_connection()