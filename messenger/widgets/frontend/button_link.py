from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.button import MDButton

class ButtonLink(MDButton):

    linked_screen = ObjectProperty()
    button_text = StringProperty()