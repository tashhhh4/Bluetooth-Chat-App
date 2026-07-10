from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from messenger.widgets.utils import wrap_text, bind_height_to_texture_height

class Cell(AnchorLayout):
    def __init__(self, text, **kwargs):
        super(Cell, self).__init__(**kwargs)

        self.anchor_y = 'top'
        self.label = Label(text=text)
        wrap_text(self.label)
        bind_height_to_texture_height(self.label)
        self.add_widget(self.label)
