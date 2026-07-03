from kivy.app import App


def change_page(widget, **kwargs):
    app = App.get_running_app()
    app.set_page(widget, **kwargs)
