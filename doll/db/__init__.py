__author__ = 'Matthew Badger'


from os.path import dirname
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from doll.db.config import config
from doll.db.model import *


'''Connection class

    Connects to the database in the root folder of the application

'''

# Connects to the database
class Connection:
    config = config

    config['sqlalchemy.url'] = 'sqlite:///' + dirname(__file__) + '/' + config['db_file']

    __engine = engine_from_config(config, echo=False)

    __Session = sessionmaker()
    __Session.configure(bind=__engine)

    session = __Session()

    @staticmethod
    def create_all():
        Base.metadata.create_all(Connection.__engine)