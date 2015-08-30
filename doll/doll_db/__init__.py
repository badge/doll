__author__ = 'Matthew Badger'

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from doll.doll_db.config import config

Base = declarative_base()


'''Connection class

    Connects to the database in the root folder of the application

'''

# Connects to the database
class Connection:
    __engine = engine_from_config(config, echo=False)

    Base.metadata.create_all(__engine)

    __Session = sessionmaker()
    __Session.configure(bind=__engine)

    session = __Session()