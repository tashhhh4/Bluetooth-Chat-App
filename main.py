from services.platform import initialize_window

initialize_window()

from kivymd.app import MDApp
from messenger.init import get_root_widget
from services.platform import get_bluetooth_service, get_message_service, initialize_permissions
from db.engine import initialize_database

class Blu2App(MDApp):

    def __init__(self):
        super().__init__()

        self.bluetooth_service = None
        self.message_service = None

    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'

        initialize_permissions()

        initialize_database()

        self.bluetooth_service = get_bluetooth_service()
        self.message_service = get_message_service()

        self.root = get_root_widget()
        self.set_page('Home')
        return self.root

    def set_page(self, page_name):
        self.root.set_page(page_name)

    def get_screen(self, page_name):
        return self.root.screen_manager.get_screen(page_name)

Blu2App().run()