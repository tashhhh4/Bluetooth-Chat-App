from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from utils import schedule

class DebugNavigation(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugNavigation, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.spacing = 5
        self.padding = 5
        self.size_hint_y = None
        self.height = 90

        self.menu_button = Button(
            text='| | |',
            size_hint=(None, None),
            size=(80, 90),
            background_color=(0, 0, 0, 1),
        )
        self.title = Label(text='Debug Views', size_hint_x=1)

        self.add_widget(self.menu_button)
        self.add_widget(self.title)

        self.dropdown = DropDown(size_hint_x=None, width=500)
        pages = [
            'BLE Scanning',
            'Devices',
            'Messages',
        ]
        for i, label in enumerate(pages):
            button = Button(
                text=label,
                size_hint_y=None,
                size_hint_x=1,
                height=100,
                background_color=(0, 0, 0, 1),
            )
            self.dropdown.add_widget(button)
        self.menu_button.bind(on_press=self.open_dropdown)

    def open_dropdown(self, button_instance):
        self.dropdown.open(self)
        schedule(self.position_dropdown)

    def position_dropdown(self, _):
        self.dropdown.x = 0
        self.dropdown.y = self.menu_button.y - self.dropdown.height