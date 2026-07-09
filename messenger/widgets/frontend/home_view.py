from kivy.properties import ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from utils import schedule
from ..app_screen import AppScreen
from .components.screen_container import ScreenContainer
from .components.screen_header import ScreenHeader
from .components.button_link import ButtonLink

class HomeView(AppScreen):

    paired_devices = ListProperty([])

    def __init__(self, **kwargs):

        super(HomeView, self).__init__(**kwargs)

        # Top-level Container
        self.container = ScreenContainer()
        self.add_widget(self.container)

        # Header
        self.header = ScreenHeader(title='Home', back_link=False)
        self.container.add_widget(self.header)

        # Button Links Container
        self.button_links_container = MDBoxLayout(orientation='vertical')
        self.container.add_widget(self.button_links_container)

        # FOR SOME REASON, THE BUTTON HAS TO BE SCHEDULED
        # OR ELSE ITS WIDTH IS TINY
        schedule(
            lambda _: self.button_links_container.add_widget(
                ButtonLink(button_text='Connect Devices', target_page='Bluetooth Manager')
            )
        )
