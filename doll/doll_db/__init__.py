__author__ = 'Matthew Badger'


from os.path import dirname
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from doll.doll_db.config import config
from doll.doll_db.model import *


'''Connection class

    Connects to the database in the root folder of the application

'''

# Connects to the database
class Connection:
    config = config

    config['sqlalchemy.url'] = 'sqlite:///' + dirname(__file__) + '/doll.db'

    __engine = engine_from_config(config, echo=False)

    __Session = sessionmaker()
    __Session.configure(bind=__engine)

    session = __Session()

    @staticmethod
    def create_all():
        Base.metadata.create_all(Connection.__engine)