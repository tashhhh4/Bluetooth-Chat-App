from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class HomeView(BoxLayout):

    def __init__(self, **kwargs):
        super(HomeView, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.add_widget(Label(text='[pretty app frontend goes here]'))