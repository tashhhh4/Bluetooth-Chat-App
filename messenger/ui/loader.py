from pathlib import Path
from kivy.lang import Builder

UI_PATH = Path(__file__).parent

def load_ui():
    print('Loading UI.')
    for kv_file in UI_PATH.rglob('*.kv'):
        Builder.load_file(str(kv_file))
