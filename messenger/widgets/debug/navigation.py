from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from messenger.pages import DEBUG_PAGES
from messenger.utils import change_page
from messenger.widgets.utils import add_background
from utils import schedule

class DebugNavigation(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugNavigation, self).__init__(**kwargs)

        add_background(self, (0, 0, 0, 1))

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)

        self.menu_button = Button(
            text='| | |',
            size_hint=(None, None),
            size=(dp(80), dp(90)),
            background_color=(0, 0, 0, 1),
            height=dp(50),
        )
        self.title = Label(text='Debug Views', size_hint_x=1)

        self.add_widget(self.menu_button)
        self.add_widget(self.title)

        self.dropdown = DropDown()
        self.menu_button.bind(on_press=self.open_dropdown)

        for page_name in DEBUG_PAGES.keys():
            button = Button(
                text=page_name,
                size_hint_y=None,
                size_hint_x=1,
                height=dp(50),
                background_color=(0, 0, 0, 1),
                background_normal='',
            )
            button.bind(on_press=lambda _, n=page_name: self.open_page(n))
            self.dropdown.add_widget(button)

    def open_page(self, page_name):
        self.dropdown.dismiss()
        change_page(page_name)

    def open_dropdown(self, _):
        self.dropdown.open(self)
        schedule(self.position_dropdown)

    def position_dropdown(self, _):
        self.dropdown.x = 0
        self.dropdown.y = self.menu_button.y - self.dropdown.height