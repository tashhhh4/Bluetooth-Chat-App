from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from messenger.widgets.utils import bind_height_to_texture_height, bind_height_to_content_height

class FormFieldRow(BoxLayout):
    def __init__(self, field_name, **kwargs):
        super(FormFieldRow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.spacing = dp(2)

        # Label
        self.label = Label(text=field_name)
        bind_height_to_texture_height(self.label)
        self.add_widget(self.label)

        # Text Input
        self.input = TextInput(multiline=False)
        bind_height_to_content_height(self.input)
        self.add_widget(self.input)