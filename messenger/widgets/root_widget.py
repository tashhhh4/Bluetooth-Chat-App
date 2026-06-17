from kivy.uix.boxlayout import BoxLayout

class RootLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.header_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None
        )
        self.add_widget(self.header_container)

        self.page_container = BoxLayout()
        self.add_widget(self.page_container)

    def add_header(self, header_widget):
        """ APPENDS the target widget to the top of the RootLayout. """
        self.header_container.add_widget(header_widget)

    def set_page(self, page_widget):
        """ REPLACES the widget in the Page area of the RootLayout. """
        self.page_container.clear_widgets()
        self.page_container.add_widget(page_widget)