import config
from kivymd.uix.widget import MDWidget
from messenger.widgets.debug.navigation import DebugNavigation

class RootLayout(MDWidget):
    def __init__(self, **kwargs):
        super().__init__(RootLayout, **kwargs)

        if config.ENVIRONMENT in ['local', 'debug']:
            self.ids.header_container.add_widget(DebugNavigation(root=self))

    def set_page(self, page_widget):
        """ REPLACES the widget in the page area of the RootLayout. """
        self.ids.page_container.clear_widgets()
        self.ids.page_container.add_widget(page_widget)