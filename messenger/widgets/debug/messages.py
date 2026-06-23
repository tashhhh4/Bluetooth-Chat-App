from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout
from ..utils import fit_height
from db.manager import chats, messages

class DebugMessages(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)

        # Top level container
        self.container = BoxLayout(orientation='vertical', spacing=5, padding=5)
        self.add_widget(self.container)

        # Refresh button
        self.refresh_button = Button(
            text='Refresh Page',
            size_hint_y=None,
            height=50
        )
        self.container.add_widget(self.refresh_button)

        # Target for create Chat button or Chat room heading
        self.chat_header = BoxLayout(size_hint_y=None)
        self.container.add_widget(self.chat_header)

        self.render_chat_header()

        # Scrollable
        self.scroll_view = ScrollView()
        self.container.add_widget(self.scroll_view)

        # Messages
        self.message_container = BoxLayout(orientation='vertical', spacing=5)
        fit_height(self.message_container)
        self.scroll_view.add_widget(self.message_container)

        self.populate_message_container()

        # Message Input
        self.message_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=90,
        )
        self.container.add_widget(self.message_input)
        self.message_button = Button(
            text='Send Message',
            size_hint_y=None,
            height=50,
        )
        self.container.add_widget(self.message_button)

    def render_chat_header(self):
        """ Renders a header for the chat room. """

    def populate_message_container(self):
        """ Displays all the messages for the selected chat room. """