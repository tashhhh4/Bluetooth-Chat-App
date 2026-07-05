from kivymd.uix.screenmanager import MDScreenManager
from .widgets.root_widget import RootLayout
from .pages import DEBUG_PAGES, PAGES, VIEWS

def get_root_widget():
    pages = dict(DEBUG_PAGES)
    pages.update(PAGES)
    pages.update(VIEWS)
    root = RootLayout(pages)
    return root