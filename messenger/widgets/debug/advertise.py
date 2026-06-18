from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from services.bluetooth import BLE

class DebugAdvertiser(BoxLayout):

    is_advertising = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DebugAdvertiser, self).__init__(**kwargs)

        self.ble = BLE()

        self.orientation = 'vertical'

        self.label = Label(
            text=self.get_label_text(),
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.label)

        self.button = Button(text=self.get_button_text(), size_hint_y=None, height=300)
        self.add_widget(self.button)
        self.button.bind(on_press=self.toggle_advertising)

    def get_button_text(self):
        if self.is_advertising:
            return 'Stop advertising'
        else:
            return 'Start advertising'

    def get_label_text(self):
        if self.is_advertising:
            return 'Advertising is ON'
        else:
            return 'Advertising is OFF'

    def toggle_advertising(self, _):
        if self.is_advertising:
            self.ble.stop_advertising()
            self.is_advertising = False
            self.button.text = self.get_button_text()
            self.label.text = self.get_label_text()
        else:
            self.ble.start_advertising()
            self.is_advertising = True
            self.button.text = self.get_button_text()
            self.label.text = self.get_label_text()
