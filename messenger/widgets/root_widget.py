from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
import config
from messenger.widgets.debug.navigation import DebugNavigation

class RootLayout(MDBoxLayout):
    def __init__(self, pages, **kwargs):

        self.pages = pages

        super(RootLayout, self).__init__(**kwargs)

        app = App.get_running_app()
        self.md_bg_color = app.theme_cls.backgroundColor

        # Top-level Container of entire app
        self.container = MDBoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Header Space for anywhere in app
        self.header_container = MDBoxLayout(orientation='horizontal', size_hint_y=None)
        self.container.add_widget(self.header_container)

        if config.ENVIRONMENT in ['local', 'debug']:
            self.header_container.add_widget(DebugNavigation())

        # Main Section with Screen Manager
        self.screen_manager = MDScreenManager()
        self.container.add_widget(self.screen_manager)

        for page_name, widget_class in self.pages.items():
            self.screen_manager.add_widget(widget_class(name=page_name))
        self.screen_manager.current = 'Home'

    def set_page(self, page_name):
        """ Changes the MDScreen loaded by screen_manager. """
        self.screen_manager.current = page_name
