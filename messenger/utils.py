from kivy.app import App

def change_page(page_name, **context):
    print('inside change_page. page_name is', page_name)
    app = App.get_running_app()
    app.set_page(page_name)
    screen = app.get_screen(page_name)
    screen.set_context(**context)
