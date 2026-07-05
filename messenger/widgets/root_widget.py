import config
from kivymd.uix.widget import MDWidget
from messenger.widgets.debug.navigation import DebugNavigation

class RootLayout(MDWidget):
    def __init__(self, pages, **kwargs):

        self.pages = pages

        super(RootLayout, self).__init__(**kwargs)

        if config.ENVIRONMENT in ['local', 'debug']:
            self.ids.header_container.add_widget(DebugNavigation())


    def on_kv_post(self, base_widget):
        screen_manager = self.ids.screen_manager
        for page_name, widget_class in self.pages.items():
            screen_manager.add_widget(widget_class(name=page_name))
        screen_manager.current = 'Home'

    def set_page(self, page_name):
        """ Changes the MDScreen loaded by screen_manager. """
        print('root_widget > set_page: page_name is', page_name)
        self.ids.screen_manager.current = page_name
