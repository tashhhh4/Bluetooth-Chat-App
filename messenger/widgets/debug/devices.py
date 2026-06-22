# Manually edit database entries for Devices and Contacts

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from .components.debug_layout import DebugLayout

class DebugDevices(DebugLayout):

    def __init__(self, **kwargs):
        super(DebugDevices, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5

        self.device_list = BoxLayout()
        self.add_widget(device_list)