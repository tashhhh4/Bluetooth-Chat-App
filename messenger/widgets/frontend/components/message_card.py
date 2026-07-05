from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

class MessageCard(MDCard):

    def __init__(self, message, **kwargs):

        self.message = message

        super(MessageCard, self).__init__(**kwargs)

        self.height = dp(60)
        self.size_hint_y = None

        # Top-level Container
        self.container = MDBoxLayout(orientation='vertical', padding=dp(5))
        self.add_widget(self.container)

        # Card Header
        self.card_header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(15))
        self.container.add_widget(self.card_header)

        # Name of the Device that sent the Message
        self.sender_label = MDLabel(text=message['sender'])
        self.card_header.add_widget(self.sender_label)

        # Time note
        self.time_label = MDLabel(text=message['time'])
        self.card_header.add_widget(self.time_label)

        # Card Body
        self.card_body = MDBoxLayout(size_hint_y=None, height=dp(45))
        self.container.add_widget(self.card_body)
        self.card_text = MDLabel(text=message['text'])
        self.card_body.add_widget(self.card_text)