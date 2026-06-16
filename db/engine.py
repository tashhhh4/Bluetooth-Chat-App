from pathlib import Path
from kivy.app import App
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Message

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

    Base.metadata.create_all(_engine)

def get_session():
    if _Session is None:
        raise RuntimeError('Database not initialized.')
    return _Session()

# Crud - move later
def get_all_messages():
    session = get_session()
    try:
        return session.query(Message).all()
    finally:
        session.close()

def add_new_message(text):
    session = get_session()
    try:
        message = Message(text=text, sender='John Snow', send_to='Anonymous')
        session.add(message)
        session.commit()
    finally:
        session.close()