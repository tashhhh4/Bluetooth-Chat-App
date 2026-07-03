from kivy.metrics import dp, sp
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from .components.debug_layout import DebugLayout

class DebugChat(DebugLayout):

    device = DictProperty()

    def __init__(self, device, **kwargs):
        super(DebugChat, self).__init__(**kwargs)

        self.device = device
        print('Initializing chat with', self.device['name'], self.device['address'])

        # Top-level page container
        self.container = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.add_widget(self.container)

        # Chat Title
        device_name = self.device['name'] if self.device['name'] else 'Unknown Device'
        self.chat_title = Label(
            text=f'Chat with {device_name}',
            font_size=sp(20),
            size_hint_y=None,
            height=dp(32)
        )
        self.container.add_widget(self.chat_title)

        # Connection Status
        self.connection_hint = Label(
            text='Connected... ?',
            font_size=sp(14),
            size_hint_y=None,
            height=dp(18)
        )
        self.container.add_widget(self.connection_hint)

        # List of Messages
        self.message_container = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.container.add_widget(self.message_container)

        # Input Form
        self.send_message_form = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        self.container.add_widget(self.send_message_form)

        # Text Input
        self.text_input = TextInput(multiline=True, size_hint_x=.8)
        self.send_message_form.add_widget(self.text_input)

        # Send Button
        self.send_button = Button(text='Send', size_hint_x=.2)
        self.send_message_form.add_widget(self.send_button)
