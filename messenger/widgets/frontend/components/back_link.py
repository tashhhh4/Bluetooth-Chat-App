from kivymd.uix.button import MDIconButton
from messenger.utils import change_page

class BackLink(MDIconButton):

    def __init__(self, target_page, **kwargs):

        self.target_page = target_page

        super(BackLink, self).__init__(**kwargs)

        self.style = 'filled'
        self.icon = 'arrow-left'

    def on_press(self):
        change_page(self.target_page)