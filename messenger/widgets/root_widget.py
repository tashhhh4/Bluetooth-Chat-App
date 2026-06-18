from kivymd.uix.widget import MDWidget

class RootLayout(MDWidget):

    def add_header(self, header_widget):
        """ APPENDS the target widget to the top of the RootLayout. """
        self.ids.header_container.add_widget(header_widget)

    def set_page(self, page_widget):
        """ REPLACES the widget in the Page area of the RootLayout. """
        self.ids.page_container.clear_widgets()
        self.ids.page_container.add_widget(page_widget)