from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText
from messenger.utils import change_page

class ButtonLink(MDButton):

    def __init__(self, button_text, target_page, **kwargs):

        self.button_text = button_text
        self.target_page = target_page

        super(ButtonLink, self).__init__(**kwargs)

        self.font_size = dp(20)
        self.height = dp(80)
        self.pos_hint = {'center_x': .5}
        self.size_hint_x = .8

        self.button_label = MDButtonText(text=self.button_text, width=dp(300))
        self.add_widget(self.button_label)

    def on_press(self):
        change_page(self.target_page)