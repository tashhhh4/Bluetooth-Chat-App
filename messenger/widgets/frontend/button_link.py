from kivy.properties import StringProperty
from kivymd.uix.button import MDButton
from messenger.utils import change_page

class ButtonLink(MDButton):

    target_page = StringProperty()
    button_text = StringProperty()

    def on_press(self):
        change_page(self.target_page)