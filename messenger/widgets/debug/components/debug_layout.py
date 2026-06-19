from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

class DebugLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size