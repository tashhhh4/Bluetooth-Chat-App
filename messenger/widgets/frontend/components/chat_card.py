from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from messenger.widgets.utils import bind_height_to_content_height
from messenger.utils import change_page
from services.platform import get_message_service

from pprint import pprint

class ChatCard(MDCard):

    def __init__(self, chat, **kwargs):

        super(ChatCard, self).__init__(**kwargs)

        self.size_hint_y = None
        self.padding = dp(30)
        bind_height_to_content_height(self)

        self.label = MDLabel(text=chat.title, font_style='Title', height=dp(20))
        self.add_widget(self.label)

        def g(_):
            message_service = get_message_service()
            message_service.open_chat_view(chat_id=chat.id)
        self.bind(on_press=g)