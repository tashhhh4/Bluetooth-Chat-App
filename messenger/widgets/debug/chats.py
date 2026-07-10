import logging
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from messenger.widgets.utils import add_background
from .components.debug_layout import DebugLayout
from db.manager import chats as chats_manager, devices as devices_manager

class DeviceCard(ButtonBehavior, BoxLayout):
    def __init__(self, device, **kwargs):

        self.selected = False
        self.device = device

        super(DeviceCard, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.turn_gray()

        # Device name
        name = device.name if device.name else 'Unnamed Device'
        self.name_label = Label(text=name, halign='left')
        self.add_widget(self.name_label)

        # Device UUID, shortened
        uuid_repr = device.uuid[:12] + '...'
        self.uuid_label = Label(text=uuid_repr, halign='left')
        self.add_widget(self.uuid_label)

    def turn_gray(self):
        add_background(self, (.5, .5, .5, 1))

    def turn_blue(self):
        add_background(self, (0.2, 0.6, 0.9, 1))

    def on_press(self):
        print('Running DeviceCard.on_press')
        self._toggle_selected()

    def _toggle_selected(self):
        if self.selected:
            self.turn_gray()
            self.selected = False
        else:
            self.turn_blue()
            self.selected = True

class DebugChats(DebugLayout):
    def __init__(self, **kwargs):

        self.device_cards = []

        super(DebugChats, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(
            orientation='vertical',
            padding=dp(5),
            spacing=dp(5),
        )
        self.add_widget(self.container)

        # Chats Listing
        self.chat_list_container = BoxLayout(orientation='vertical', spacing=dp(5))
        self.container.add_widget(self.chat_list_container)

        # Title
        self.list_title = Label(text='Chats', size_hint_y=None, height=dp(50))
        self.chat_list_container.add_widget(self.list_title)

        # List of Chats
        self.chat_list = BoxLayout(orientation='vertical', spacing=dp(20))
        self.chat_list_container.add_widget(self.chat_list)

        # Chats Form
        self.chat_form_container = BoxLayout(orientation='vertical', spacing=dp(5))
        self.container.add_widget(self.chat_form_container)

        # Chats Form Title
        self.form_title = Label(
            text='Create New Chat',
            size_hint_y=None,
        )
        self.chat_form_container.add_widget(self.form_title)

        # Chats Form Row for Title Input
        self.chat_form_title_label = Label(text='Title', size_hint_y=None)
        # bind_height_to_texture_height(self.chat_form_title_label)
        self.chat_form_container.add_widget(self.chat_form_title_label)
        self.chat_form_title_input = TextInput(multiline=False, size_hint_y=None)
        self.chat_form_container.add_widget(self.chat_form_title_input)


        # Chats Form Device Selection Title
        self.device_selection_title = Label(text='Select Devices', size_hint_y=None)
        self.chat_form_container.add_widget(self.device_selection_title)

        # Chats Form Device Selection
        self.device_selection_list = GridLayout(
            cols=3,
            spacing=dp(5),
            row_default_height=dp(50),
            row_force_default=True,
        )
        self.chat_form_container.add_widget(self.device_selection_list)

        # Spacer
        self.spacer = Widget()
        self.chat_form_container.add_widget(self.spacer)

        # Chats Form Create Button
        self.chat_form_button = Button(text='Create', size_hint_y=None, height=dp(50))
        self.chat_form_container.add_widget(self.chat_form_button)

        ######## ACTIONS ########

        # Add Chat Button
        def create_chat(_):
            try:
                title = self.chat_form_title_input.text.strip()
                device_uuids = []
                for card in self.device_cards:
                    if card.selected:
                        u = card.device.uuid
                        device_uuids.append(u)
                new_chat = chats_manager.create(device_uuids)
                logging.info(f'DebugChats: Created a new chat: "{new_chat.title}"')
                self.load_chats()
            except ValueError as e:
                logging.error(f'DebugChats: {e}')
        self.chat_form_button.bind(on_press=create_chat)

    def load_chats(self):
        chats = chats_manager.list_chats()
        self.populate_chat_list(chats)

    def load_devices(self):
        devices = devices_manager.list_devices()
        self.populate_device_selection_list(devices)

    def populate_chat_list(self, chats):
        self.chat_list.clear_widgets()

        for chat in chats:
            # Card Container
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
            add_background(card, (.3, .2, .1, 1))
            self.chat_list.add_widget(card)

            # Header with Title and ID
            header = BoxLayout(size_hint_y=None, height=dp(24))
            card.add_widget(header)
            title = Label(text=chat.title, font_size=sp(16), size_hint_x=.9)
            id_label = Label(text=str(chat.id), size_hint_x=.1)
            header.add_widget(title)
            header.add_widget(id_label)

            # Body with 2 columns
            body = BoxLayout()
            col_1 = BoxLayout(orientation='vertical')
            col_2 = BoxLayout(orientation='vertical')
            card.add_widget(body)
            body.add_widget(col_1)
            body.add_widget(col_2)

            # Devices List
            devices_title = Label(text='Devices', size_hint_y=None, height=dp(24), font_size=sp(16))
            col_1.add_widget(devices_title)
            devices_list = BoxLayout(orientation='vertical')
            col_1.add_widget(devices_list)

            # for device in room.members: # TODO: Make this work

            # Latest Message
            latest_message_title = Label(text='Latest Message', size_hint_y=None, height=dp(24), font_size=sp(16))
            col_2.add_widget(latest_message_title)
            latest_message = Label(text='... Latest Message Here ...', font_size=sp(12))
            col_2.add_widget(latest_message)

            # Delete Button
            delete_button = Button(text='Delete this Chat', size_hint_y=None, height=dp(36), background_color='red')
            col_2.add_widget(delete_button)

            # Delete Button Behavior
            def delete_chat(_):
                chats_manager.delete(chat.id)
                self.load_chats()
            delete_button.bind(on_press=delete_chat)

        # Final empty widget to push space upwards
        self.chat_list.add_widget(BoxLayout())

    def populate_device_selection_list(self, devices):
        self.device_selection_list.clear_widgets()
        self.device_cards = []

        for device in devices:
            card = DeviceCard(device)
            self.device_selection_list.add_widget(card)
            self.device_cards.append(card)

        num_children = len(self.device_selection_list.children)
        remainder = 3 % num_children
        for r in range(remainder):
            self.device_selection_list.add_widget(Widget())

    def on_pre_enter(self, *args):
        self.load_chats()
        self.load_devices()