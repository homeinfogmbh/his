"""
Handles requests on services
"""
from homeinfo.his.db import Session, User, SessionExistsError

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '21.10.2014'
__all__ = ['SessionExistsError', 'SessionController']


class SessionExistsError(Exception):
    """
    Indicates that a session for a user is already running
    """
    pass


class SessionController():
    """
    A class handle sessions
    """
    @classmethod
    def logged_in(cls, user):
        """Determines whether a user is logged in"""
        for session in Session.select().where(Session.user == user):
            if session.valid:
                return True
        return False

    @classmethod
    def login(cls, hashed_user_name, passwd):
        """Login a user"""
        for user in User.select().where(User.hashed_name == hashed_user_name):
            for session in cls.select().where(cls.user == user):
                raise SessionExistsError(session)
            if user.passwd == passwd:
                Session.start(user)
                return True
        return False
