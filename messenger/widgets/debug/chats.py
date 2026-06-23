from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout

class DebugChats(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugChats, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(
            orientation='vertical',
            padding=5,
            spacing=5,
        )
        self.add_widget(self.container)

        # Chats Listing
        self.chat_list_container = BoxLayout(orientation='vertical', spacing=5)
        self.container.add_widget(self.chat_list_container)

        # Title
        self.list_title = Label(text='Chat Rooms', size_hint_y=None, height=50)
        self.chat_list_container.add_widget(self.list_title)

        # List of Chats
        self.chat_list = BoxLayout(orientation='vertical', spacing=5)
        self.chat_list_container.add_widget(self.chat_list)

        self.populate_chat_list()

        # Chats Form
        self.chat_form_container = BoxLayout(orientation='vertical', spacing=5)
        self.container.add_widget(self.chat_form_container)
        self.form_title = Label(
            text='Create New Chat Room',
            size_hint_y=None,
            height=50,
        )

        # Title
        self.chat_form_container.add_widget(self.form_title)

        # Rest of the Form
        self.chat_form = BoxLayout(orientation='vertical', spacing=5)
        self.chat_form_container.add_widget(self.chat_form)
        self.chat_form_title_label = Label(text='Title')
        self.chat_form_title_input = TextInput(multiline=False)
        self.chat_form_devices_label = Label(text='Devices (one UUID per line)')
        self.chat_form_devices_input = TextInput(multiline=True, size_hint_y=None, height=100)
        self.chat_form_button = Button(text='Create', size_hint_y=None, height=50, pos_hint={'center_x': .5})
        self.chat_form.add_widget(self.chat_form_title_label)
        self.chat_form.add_widget(self.chat_form_title_input)
        self.chat_form.add_widget(self.chat_form_devices_label)
        self.chat_form.add_widget(self.chat_form_devices_input)
        self.chat_form.add_widget(self.chat_form_button)

    def populate_chat_list(self):
        pass