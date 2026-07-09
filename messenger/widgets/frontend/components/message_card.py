from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from messenger.widgets.utils import bind_height_to_texture_height, bind_height_to_content_height

import kivymd

class MessageCard(MDCard):

    def __init__(self, message, **kwargs):

        self.message = message

        super(MessageCard, self).__init__(**kwargs)

        self.size_hint_y = None
        bind_height_to_content_height(self)

        # Top-level Container
        self.container = MDBoxLayout(orientation='vertical', padding=dp(5))
        bind_height_to_content_height(self.container)
        self.add_widget(self.container)

        # Card Header
        self.card_header = MDBoxLayout(orientation='horizontal')
        bind_height_to_content_height(self.card_header)
        self.container.add_widget(self.card_header)

        # Name of the Device that sent the Message
        self.sender_label = MDLabel(text=message['sender'])
        bind_height_to_texture_height(self.sender_label)
        self.card_header.add_widget(self.sender_label)

        # Time note
        self.time_label = MDLabel(text=message['time'])
        bind_height_to_texture_height(self.time_label)
        self.card_header.add_widget(self.time_label)

        # Card Body
        self.card_body = MDBoxLayout()
        bind_height_to_content_height(self.card_body)
        self.container.add_widget(self.card_body)
        self.card_text = MDLabel(text=message['text'])
        bind_height_to_texture_height(self.card_text)
        self.card_body.add_widget(self.card_text)