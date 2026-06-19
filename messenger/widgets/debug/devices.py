from kivy.uix.label import Label
from .components.debug_layout import DebugLayout

class DebugDevices(DebugLayout):

    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        self.add_widget(Label(text='Add, Delete, Edit, and view Devices'))