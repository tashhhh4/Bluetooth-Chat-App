import logging
from kivy.app import App

def change_page(page_name, **context):
    logstr = f'change_page: Navigate to {page_name}'
    if context:
        logstr += f' with context {str(context)}'
    logging.info(logstr)
    app = App.get_running_app()
    screen = app.get_screen(page_name)
    screen.set_context(**context)
    app.set_page(page_name)
