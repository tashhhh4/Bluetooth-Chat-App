from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DebugDevices(BoxLayout):

    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        self.add_widget(Label(text='Add, Delete, Edit, and view Devices'))