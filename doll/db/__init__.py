from os.path import expanduser
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from ..config import config
from .model import *


# Connects to the database
class Connection:
    """Connection

    Connects to the database in the user's .doll directory
    """

    config = config

    config['sqlalchemy.url'] = 'sqlite:///' + expanduser("~/.doll") + '/' + config['db_file']

    __engine = engine_from_config(config, echo=False)

    __Session = sessionmaker()
    __Session.configure(bind=__engine)

    session = __Session()

    @staticmethod
    def create_all():
        Base.metadata.create_all(Connection.__engine)