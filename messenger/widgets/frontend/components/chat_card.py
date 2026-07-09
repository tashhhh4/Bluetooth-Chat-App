from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from messenger.widgets.utils import bind_height_to_content_height
from messenger.utils import change_page

class ChatCard(MDCard):

    def __init__(self, chat, **kwargs):

        super(ChatCard, self).__init__(**kwargs)

        self.size_hint_y = None
        self.padding = dp(30)
        bind_height_to_content_height(self)

        self.label = MDLabel(text=chat.title, font_style='Title', height=dp(20))
        self.add_widget(self.label)

        def g(_):
            change_page('Chat', chat_id=chat.id, chat_title=chat.title)

        self.bind(on_press=g)