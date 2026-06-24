from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from .components.debug_layout import DebugLayout
from messenger.pages import DEBUG_PAGES
from utils import schedule

class DebugNavigation(DebugLayout):

    HEIGHT = 90

    def __init__(self, root, **kwargs):
        super(DebugNavigation, self).__init__(**kwargs)

        self.root = root

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = self.HEIGHT

        self.menu_button = Button(
            text='| | |',
            size_hint=(None, None),
            size=(80, 90),
            background_color=(0, 0, 0, 1),
            height=self.HEIGHT,
        )
        self.title = Label(text='Debug Views', size_hint_x=1)

        self.add_widget(self.menu_button)
        self.add_widget(self.title)

        self.dropdown = DropDown()
        self.menu_button.bind(on_press=self.open_dropdown)

        for title, widget in DEBUG_PAGES.items():
            button = Button(
                text=title,
                size_hint_y=None,
                size_hint_x=1,
                height=50,
                background_color=(0, 0, 0, 1),
                background_normal='',
            )
            button.bind(on_press=lambda _, w=widget: self.open_page(w))
            self.dropdown.add_widget(button)

    def open_page(self, widget_class):
        self.dropdown.dismiss()
        self.root.set_page(widget_class())

    def open_dropdown(self, _):
        self.dropdown.open(self)
        schedule(self.position_dropdown)

    def position_dropdown(self, _):
        self.dropdown.x = 0
        self.dropdown.y = self.menu_button.y - self.dropdown.height