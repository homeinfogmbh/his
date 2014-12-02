"""
Handles requests on services
"""
from homeinfo.his.db import Session, User
from homeinfo.his.lib.error import (SessionExistsError,
                                    SessionTimeoutError,
                                    InvalidCredentialsError)

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '21.10.2014'
__all__ = ['SessionExistsError', 'SessionController']


class SessionController():
    """
    A class handle sessions
    """
    @classmethod
    def active(cls, user):
        """Determines whether a user is running an active, valid session"""
        if not user.locked:
            return cls._logged_in(user)
        else:
            return False

    @classmethod
    def _logged_in(cls, user):
        """Determines whether a user is logged in"""
        for session in Session.select().where(Session.user == user):
            if session.valid:
                return True
            else:
                session.terminate()
                raise SessionTimeoutError()
        return False

    @classmethod
    def login(cls, hashed_user_name, passwd):
        """Login a user"""
        for user in (User.select().limit(1)
                     .where(User.hashed_name == hashed_user_name)):
            for session in Session.select().where(Session.user == user):
                raise SessionExistsError(session)
            if user.passwd == passwd:
                user.failed_logins = 0
                user.save()
                Session.start(user)
                return True
        for user in (User.select().limit(1)
                     .where(User.hashed_name == hashed_user_name)):
            user.failed_logins += 1
            user.save()
        raise InvalidCredentialsError()
