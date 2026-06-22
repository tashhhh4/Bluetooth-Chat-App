from kivymd.app import MDApp
from messenger.widgets import HomeView, RootLayout
from messenger.ui.loader import load_ui
from services.platform import initialize_permissions
from db.engine import initialize_database

class Blu2App(MDApp):
    def build(self):
        self.theme_cls.material_style = 'M2'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'

        load_ui()

        initialize_permissions()

        initialize_database()

        root_widget = RootLayout()
        root_widget.set_page(HomeView())

        return root_widget

Blu2App().run()