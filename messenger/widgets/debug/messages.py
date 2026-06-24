from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from .components.debug_layout import DebugLayout
from ..utils import fit_height, add_background, wrap_text
from db.manager import chats, devices, messages

class DebugMessages(DebugLayout):

    chat = ObjectProperty()

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
        self.message_container = BoxLayout(orientation='vertical', spacing=10)
        fit_height(self.message_container)
        self.scroll_view.add_widget(self.message_container)

        # Input Form
        self.form = BoxLayout(size_hint_y=None, height=80, spacing=10)
        self.container.add_widget(self.form)
        self.text_input = TextInput(multiline=True, size_hint_x=.8)
        self.submit_button = Button(text='Send', size_hint_x=.2)
        self.form.add_widget(self.text_input)
        self.form.add_widget(self.submit_button)

        ###### ACTIONS ######

        # Load Chat
        def load_chat(_):
            chat_id = self.chat_room_loader_input.text
            self.chat = chats.get(chat_id)
        self.chat_room_loader_button.bind(on_press=load_chat)

        # Refresh Messages
        def refresh_messages(_):
            self.populate_messages()
        self.refresh_button.bind(on_press=refresh_messages)

        # Send Message
        def submit_message(_):
            if not self.chat:
                return
            text = self.text_input.text
            my_device = devices.get_mine()
            messages.create(chat_id=self.chat.id, device_uuid=my_device.uuid, text=text)
        self.submit_button.bind(on_press=submit_message)

    def populate_messages(self):
        if not self.chat:
            return

        latest_messages = messages.list_messages(self.chat.id)
        device_names = []
        for message in latest_messages:
            device = devices.get(message.device_uuid)
            device_names.append(device.name)

        self.message_container.clear_widgets()
        for i, message in enumerate(latest_messages):
            # Card Wrapper
            card = BoxLayout(orientation='vertical', size_hint_y=None, padding=5)
            fit_height(card)
            add_background(card, (.1, 0, 1, .5))
            self.message_container.add_widget(card)

            # Card Header
            card_header = BoxLayout(size_hint_y=None, height=20)
            card.add_widget(card_header)

            # Name of the Device that sent the Message
            device_name = Label(text=device_names[i])
            card_header.add_widget(device_name)

            # Timestamp
            timestamp = Label(text='[Today at 10:28]', color='gray')
            card_header.add_widget(timestamp)

            # E Button
            e_button = Button(text='E', background_color='yellow', size_hint_x=None, width=22)
            card_header.add_widget(e_button)

            # X Button
            x_button = Button(text='X', background_color='red', size_hint_x=None, width=22)
            card_header.add_widget(x_button)

            # Card Body
            card_body = BoxLayout(size_hint_y=None, height=50)
            card_text = Label(text=message.text)
            wrap_text(card_text)
            card.add_widget(card_body)
            card_body.add_widget(card_text)

            # E Button Action
            def e(_):
                new_text = message.text + ' (edited)'
                messages.update(message.id, new_text)
            e_button.bind(on_press=e)

            # X Button Action
            def x(_):
                messages.delete(message.id)
            x_button.bind(on_press=x)

        # Spacer
        spacer = Widget()
        self.message_container.add_widget(spacer)