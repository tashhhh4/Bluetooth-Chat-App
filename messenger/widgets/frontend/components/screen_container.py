from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout

class ScreenContainer(MDBoxLayout):
    """ This should be used as the top-level container for almost
        every "Screen" in the app. A Screen is a top-level, full-screen
        interface which is accessible by the app's navigation links,
        upon which additional components are attached to provide
        the user with a set of related information and functionality.
    """


    def __init__(self, **kwargs):
        super(ScreenContainer, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(20)
