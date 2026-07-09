from kivy.metrics import dp
from kivy.properties import ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import MDWidget
from ..app_screen import AppScreen
from .components.screen_container import ScreenContainer
from .components.screen_header import ScreenHeader
from .components.chat_card import ChatCard
from messenger.widgets.utils import bind_height_to_content_height
from services.platform import get_message_service

class ChatsView(AppScreen):

    chats = ListProperty([])

    def __init__(self, **kwargs):

        super(ChatsView, self).__init__(**kwargs)

        # Top-level Container
        self.container = ScreenContainer()
        self.add_widget(self.container)

        # Header
        self.header = ScreenHeader(title='My Chats', back_link=True, back_loc='Home')
        self.container.add_widget(self.header)

        # Chats List
        self.chats_container = MDBoxLayout(orientation='vertical', spacing=dp(10))
        bind_height_to_content_height(self.chats_container)
        self.container.add_widget(self.chats_container)

        # Spacer
        self.spacer = MDWidget()
        self.container.add_widget(self.spacer)

        self.load_chats()

    def populate_chats_list(self, chats):
        for chat in chats:
            chat_card = ChatCard(chat)
            self.chats_container.add_widget(chat_card)

    def on_chats(self, _, chats):
        print('Chats are', chats)
        self.populate_chats_list(chats)

    def load_chats(self):
        print('ChatsView.load_chats()')
        message_service = get_message_service()
        chats = message_service.load_chats()
        print('Chats are', chats)
        self.chats = chats