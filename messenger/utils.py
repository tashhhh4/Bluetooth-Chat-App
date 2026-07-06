from kivy.app import App

def change_page(page_name, **context):
    app = App.get_running_app()
    app.set_page(page_name)
    screen = app.get_screen(page_name)
    if hasattr(screen, 'set_context'):
        screen.set_context(**context)