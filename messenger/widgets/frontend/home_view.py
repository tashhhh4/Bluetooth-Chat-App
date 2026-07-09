from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from ..app_screen import AppScreen
from .components.button_link import ButtonLink
from .components.screen_container import ScreenContainer

class HomeView(AppScreen):

    def __init__(self, **kwargs):

        super(HomeView, self).__init__(**kwargs)

        # Top-level container
        self.container = ScreenContainer()
        self.add_widget(self.container)

        # Page Label
        self.page_label = MDLabel(text='Home Page :D', font_style='Headline')
        self.container.add_widget(self.page_label)

        # Primary Button-Links
        self.button_links_container = MDBoxLayout(orientation='vertical')
        self.container.add_widget(self.button_links_container)

        # Bluetooth Manager Link
        self.bluetooth_button_link = ButtonLink(
            button_text='Scan and Connect Devices',
            target_page='Bluetooth Manager'
        )
        self.button_links_container.add_widget(self.bluetooth_button_link)