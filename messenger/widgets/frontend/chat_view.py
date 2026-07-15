import logging
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget
from utils import schedule
from services.platform import get_message_service
from messenger.widgets.utils import bind_height_to_content_height
from ..app_screen import AppScreen
from .components.connection_status_card import ConnectionStatusCard
from .components.message_card import MessageCard
from .components.screen_container import ScreenContainer
from .components.screen_header import ScreenHeader

class ChatView(AppScreen):

    chat_id = NumericProperty()
    chat_title = StringProperty()
    peer_device = ObjectProperty()
    messages = ListProperty([])
    connected = BooleanProperty(False)

    def __init__(self, **kwargs):

        super(ChatView, self).__init__(**kwargs)

        # Top-level Container
        self.container = ScreenContainer()
        self.add_widget(self.container)

        # Header
        self.header = ScreenHeader(subtitle='Connected... ?', back_link=True, back_loc='Home')
        self.container.add_widget(self.header)

        # Optionally Visible Connection Status Box
        self.connection_status_container = MDBoxLayout()
        bind_height_to_content_height(self.connection_status_container)
        self.container.add_widget(self.connection_status_container)

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

    def update_connection_box(self, connected, device):
        print('Running update_connection_box')
        self.connection_status_container.clear_widgets()
        if connected and device == self.peer_device:
            self.header.subtitle = 'Connected'
        elif connected and device != self.peer_device:
            self.header.subtitle = None
            connection_status_card = ConnectionStatusCard(
                blue_text='[b]You are currently connected to a different device.[/b]',
                black_text=f'Click here to disconnect from {device.name} and connect to {self.peer_device.name}',
            )
            self.connection_status_container.add_widget(connection_status_card)
        else:
            self.header.subtitle = None
            connection_status_card = ConnectionStatusCard(
                blue_text='[b]You are not connected to this device.[/b]',
                black_text='Connect to continue your conversation.',
            )
            self.connection_status_container.add_widget(connection_status_card)

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
        connected = False
        device = None
        if message_service.connected_state == 'CONNECTED':
            device = message_service.connected_device
            if device:
                logging.debug(f'ChatView: Connected with {device.__repr__()}')
                logging.debug(f'ChatView: My Peer device is {self.peer_device.__repr__()}')
                if device == self.peer_device:
                    logging.debug('ChatView: Devices match.')
                    connected = True
                else:
                    logging.debug('ChatView: Sorry, but your connected Device is in another Chat.')
                    connected = False
        else:
            logging.debug('ChatView: Not connected.')
            connected = False

        self.connected = connected
        self.update_connection_box(connected, device)

    def set_context(self, **context):
        self.chat_id = context.get('chat_id')
        self.chat_title = context.get('chat_title')
        self.peer_device = context.get('peer_device')

    def on_connection(self, _, value):
        self.update_connection_box(value, self.peer_device)

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
        message_service = get_message_service()
        message_service.event_registry.register_event_callback('MESSAGE_RECEIVED', self._handle_message_received)
        message_service.event_registry.register_event_callback('DEVICE_CONNECTED', self._handle_device_connected)
        message_service.event_registry.register_event_callback('DEVICE_DISCONNECTED', self._handle_device_disconnected)
        self._load_messages()
        self.check_connection()

    def on_pre_leave(self):
        message_service = get_message_service()
        message_service.event_registry.unregister_event_callback('MESSAGE_RECEIVED', self._handle_message_received)
        message_service.event_registry.unregister_event_callback('DEVICE_CONNECTED', self._handle_device_connected)
        message_service.event_registry.unregister_event_callback('DEVICE_DISCONNECTED', self._handle_device_disconnected)

    def _load_messages(self):
        logging.info('ChatView: Running _load_messages()')
        message_service = get_message_service()
        messages = message_service.load_messages(self.chat_id)
        logging.info(f'ChatView: Got {len(messages)} messages from MessageService.')
        self.messages = messages

    def _handle_message_received(self):
        logging.debug('ChatView: Running _handle_message_received()')
        self._load_messages()

    def _handle_device_connected(self):
        logging.debug('ChatView: Running _handle_device_connected()')
        self.check_connection()

    def _handle_device_disconnected(self):
        logging.debug('ChatView: Running _handle_device_disconnected()')
        self.check_connection()
