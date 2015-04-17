"""
Service definitions
"""
from uuid import uuid4
from datetime import datetime, timedelta
from peewee import CharField, ForeignKeyField, DateTimeField
from homeinfolib.db import create, improved
from .abc import HISModel
from .passwd import User

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '02.11.2014'
__all__ = ['Session']


@create
@improved
class Session(HISModel):
    """A session of a user using the system"""

    DEFAULT_LIFETIME = 600  # Default lifetime in seconds for a session

    user = ForeignKeyField(User, related_name='sessions', db_column='user')
    """The owner of the session"""
    token = CharField(36)
    """An administrative token"""
    timeout = DateTimeField()
    """The date and time when the session will time out"""

    def __bool__(self):
        """Verifies the session"""
        return self.valid

    @classmethod
    def start(cls, user, lifetime=None):
        """Start a session for a user"""
        lifetime = lifetime or cls.DEFAULT_LIFETIME
        session = cls()
        session.user = user
        session.token = str(uuid4())
        session.timeout = datetime.now() + timedelta(seconds=lifetime)
        session.save()
        return session

    @property
    def valid(self):
        """Determines whether a session is (still) valid"""
        return self.timeout - datetime.now() > timedelta(seconds=0)

    def refresh(self, lifetime=None):
        """Refreshes the session"""
        lifetime = lifetime or self.DEFAULT_LIFETIME
        self.token = str(uuid4())
        self.timeout = datetime.now() + timedelta(seconds=lifetime)
        self.save()
        return self

    def terminate(self):
        """Terminates the session"""
        cls = self.__class__
        for session in cls.select().where(cls.user == self.user):
            session.delete_instance()
