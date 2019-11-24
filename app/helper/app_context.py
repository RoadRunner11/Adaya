from flask_bcrypt import Bcrypt
from app.helper import SingletonMetaClass
from flask_sqlalchemy import SQLAlchemy
import logging

class AppContext(metaclass=SingletonMetaClass):
    """
    AppContext is the global context for logging, db etc..

    Args:
        metaclass ([type], optional):  Defaults to SingletonMetaClass.
    """

    def __init__(self):
        # set logger level
        self.logger = logging.getLogger('global_logger')
        self.logger.setLevel(logging.DEBUG)
        self.db = SQLAlchemy()
        self.bcrypt = Bcrypt()
