from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from messenger.utils import change_page

class ButtonLink(MDBoxLayout):
    def __init__(self, button_text, target_page, **kwargs):

        super(ButtonLink, self).__init__(**kwargs)

        self.button_layout = MDAnchorLayout(anchor_x='center')
        self.add_widget(self.button_layout)

        self.button = MDButton(
            style='elevated',
        )
        self.button_layout.add_widget(self.button)
        self.button_text = MDButtonText(text=button_text, font_style='Title')
        self.button.add_widget(self.button_text)

        ### Button Action ###

        self.button.bind(on_press=lambda _: change_page(target_page))
