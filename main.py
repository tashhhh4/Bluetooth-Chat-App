from services.platform import initialize_window

initialize_window()

from kivymd.app import MDApp
from messenger.widgets import HomeView, RootLayout
from messenger.ui.loader import load_ui
from services.platform import get_bluetooth_service, initialize_permissions
from db.engine import initialize_database

class Blu2App(MDApp):

    def __init__(self):
        super().__init__()

        self.bluetooth_service = None

    def build(self):
        self.theme_cls.material_style = 'M2'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'

        load_ui()

        initialize_permissions()

        initialize_database()

        self.bluetooth_service = get_bluetooth_service()

        self.root = RootLayout()
        self.set_page(HomeView)
        return self.root

    def set_page(self, widget, **kwargs):
        page = widget(**kwargs)
        self.root.set_page(page)

Blu2App().run()