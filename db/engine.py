from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from config import DELETE_TABLES

_engine = None
_Session = None

def initialize_database(user_data_dir):
    global _engine
    global _Session

    if _engine is not None:
        return

    data_dir = Path(user_data_dir)
    database_path = data_dir / 'b2.sqlite'
    _engine = create_engine(f'sqlite:///{database_path}')
    _Session = sessionmaker(bind=_engine, expire_on_commit=False)
    if DELETE_TABLES:
        models.Base.metadata.drop_all(_engine)
    models.Base.metadata.create_all(_engine)

def get_session():
    if _Session is None:
        raise RuntimeError('Database not initialized.')
    return _Session()
