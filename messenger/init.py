from pathlib import Path
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from .widgets.root_widget import RootLayout
from .pages import DEBUG_PAGES, PAGES, VIEWS

def get_root_widget():
    screen_manager = MDScreenManager()
    pages = dict(DEBUG_PAGES)
    pages.update(PAGES)
    pages.update(VIEWS)
    root = RootLayout(pages)
    return root

UI_PATH = Path(__file__).parent

def load_ui():
    for kv_file in UI_PATH.rglob('*.kv'):
        Builder.load_file(str(kv_file))
