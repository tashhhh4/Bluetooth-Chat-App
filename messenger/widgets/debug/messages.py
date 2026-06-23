from kivy.uix.scrollview import ScrollView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout
from ..utils import fit_height


class DebugMessages(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Chat Room Loader
        self.chat_room_loader = BoxLayout(size_hint_y=None, height=50)
        self.container.add_widget(self.chat_room_loader)

        # Refresh Button
        self.refresh_button = Button(size_hint_y=None, height=50)
        self.container.add_widget(self.refresh_button)

        # Scrolling Container
        self.scroll_view = ScrollView()
        self.container.add_widget(self.scroll_view)

        # Messages section
        self.message_container = BoxLayout(orientation='vertical')
        fit_height(self.message_container)
        self.container.add_widget(self.message_container)

        # Input Form
        self.form = BoxLayout(size_hint_y=None, height=80)
        self.container.add_widget(self.form)
        self.text_input = TextInput(multiline=True, size_hint_x=.8)
        self.submit_button = Button(text='Send', size_hint_x=.2)
        self.form.add_widget(self.text_input)
        self.form.add_widget(self.submit_button)