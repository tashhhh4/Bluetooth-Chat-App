from kivy.app import App
import db.engine as db
from messenger.widgets import DebugMessages

class Blu2App(App):
    def build(self):
        db.initialize_database()
        return DebugMessages()

Blu2App().run()