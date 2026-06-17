from pathlib import Path
from kivy.app import App
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

_engine = None
_Session = None

def initialize_database():
    global _engine
    global _Session

    if _engine is not None:
        return

    app = App.get_running_app()
    data_dir = Path(app.user_data_dir)
    database_path = data_dir / 'b2.sqlite'
    _engine = create_engine(f'sqlite:///{database_path}')
    _Session = sessionmaker(bind=_engine)

    models.Base.metadata.create_all(_engine)

def get_session():
    if _Session is None:
        raise RuntimeError('Database not initialized.')
    return _Session()
