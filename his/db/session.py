"""
Service definitions
"""
from .abc import HISModel
from .passwd import User
from peewee import CharField, ForeignKeyField, DateTimeField
from uuid import uuid4
from datetime import datetime, timedelta

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '02.11.2014'
__all__ = ['SessionExistsError', 'Session']


class SessionExistsError(Exception):
    """An exception to indicate that a
    session for a user is already running"""
    def __init__(self, session):
        """Sets the already-running session"""
        self.__session = session

    @property
    def session(self):
        """Returns the already-running session"""
        return self.__session


class Session(HISModel):
    """
    A session of a user using the system
    """
    user = ForeignKeyField(User, related_name='sessions', db_column='user')
    """The owner of the session"""
    token = CharField(36)
    """An administrative token"""
    timeout = DateTimeField()
    """The date and time when the session will time out"""

    @classmethod
    def start(cls, user, lifetime=600):
        """Start a session for a user"""
        for session in cls.select().where(cls.user == user):
            raise SessionExistsError(session)
        session = cls()
        session.user = user
        session.token = str(uuid4())
        session.timeout = datetime.now() + timedelta(seconds=lifetime)
        session.save()
        return session

    @property
    def valid(self):
        """Determines whether a session is (still) valid"""
        if self.timeout - datetime.now() > timedelta(seconds=0):
            return True
        else:
            return False

    def terminate(self):
        """Terminates the session"""
        cls = self.__class__
        for session in cls.select().where(cls.user == self.user):
            session.delete_instance()
