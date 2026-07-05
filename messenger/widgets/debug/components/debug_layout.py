from kivy.graphics import Color, Rectangle
from kivymd.uix.screen import MDScreen

class DebugLayout(MDScreen):
    def __init__(self, **kwargs):

        super(DebugLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)


    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def set_context(self, **context):
        pass