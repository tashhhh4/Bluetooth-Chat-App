from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout
from ..utils import fit_height


class DebugMessages(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugMessages, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.container)

        # Chat Room Loader
        self.chat_room_loader = BoxLayout(size_hint_y=None, height=30, spacing=10)
        self.container.add_widget(self.chat_room_loader)
        self.chat_room_loader_label = Label(text='Chat room:', size_hint_x=.3)
        self.chat_room_loader_input = TextInput(size_hint_x=.2)
        self.chat_room_loader_button = Button(text='Load', size_hint_x=.4)
        self.chat_room_loader.add_widget(self.chat_room_loader_label)
        self.chat_room_loader.add_widget(self.chat_room_loader_input)
        self.chat_room_loader.add_widget(self.chat_room_loader_button)

        # Refresh Button
        self.refresh_button = Button(text='Refresh Messages', size_hint_y=None, height=50)
        self.container.add_widget(self.refresh_button)

        # Scrolling Container
        self.scroll_view = ScrollView()
        self.container.add_widget(self.scroll_view)

        # Messages section
        self.message_container = BoxLayout(orientation='vertical')
        fit_height(self.message_container)
        self.container.add_widget(self.message_container)

        # Input Form
        self.form = BoxLayout(size_hint_y=None, height=80, spacing=10)
        self.container.add_widget(self.form)
        self.text_input = TextInput(multiline=True, size_hint_x=.8)
        self.submit_button = Button(text='Send', size_hint_x=.2)
        self.form.add_widget(self.text_input)
        self.form.add_widget(self.submit_button)