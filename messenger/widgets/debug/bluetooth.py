from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from .components.debug_layout import DebugLayout
from services import bluetooth

class DebugBluetooth(DebugLayout):
    def __init__(self, **kwargs):
        super(DebugBluetooth, self).__init__(**kwargs)

        # Top-level page container
        self.container = BoxLayout(orientation='vertical')
        self.add_widget(self.container)

        # Make Visible Button
        self.make_visible_button = Button(
            text='Turn discoverability on',
            size_hint_x=0.5,
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5},
        )
        self.container.add_widget(self.make_visible_button)

        # Spacer
        self.spacer = Widget()
        self.container.add_widget(self.spacer)


        ### Bind Actions ###

        # Test Turn Discovery On
        def make_visible(_):
            bluetooth.turn_discoverability_on()
        self.make_visible_button.bind(on_press=make_visible)