"""
Handles requests on services
"""
from homeinfo.his.db import Session, User
from homeinfo.his.lib.error import (SessionExistsError, SessionTimeoutError,
                                    InvalidCredentialsError, NoSuchUser,
                                    UserLocked, NotLoggedIn)

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '21.10.2014'
__all__ = ['SessionController']


class SessionController():
    """
    A class handle sessions
    """
    @classmethod
    def login(cls, hashed_user_name, passwd):
        """Login a user"""
        user = User.by_hashed_name(hashed_user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            for _ in Session.select().limit(1).where(Session.user == user):
                raise SessionExistsError()
            else:
                if user.passwd == passwd:
                    user.failed_logins = 0
                    user.save()
                    Session.start(user)
                    return True
                else:
                    user.failed_logins += 1
                    user.save()
                    raise InvalidCredentialsError()

    @classmethod
    def refresh(cls, hashed_user_name, session_token):
        """Refresh a session for a user"""
        user = User.by_hashed_name(hashed_user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    return session.refresh()
                else:
                    session.terminate()
                    raise SessionTimeoutError()
            else:
                raise NotLoggedIn()
