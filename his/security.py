"""
Handles service access
"""
from homeinfo.his.db import Service, UserService, GroupService, User, Session
from homeinfo.his.lib.error import *

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '04.12.2014'
__all__ = ['login', 'authenticate', 'authorize']


def login(func):
    """Login for a method"""
    def _login(*args, user_name=None, user_pass=None, **kwargs):
        """Login a user"""
        if user_name is None or user_pass is None:
            raise NotAuthenticated()
        user = User.by_hashed_name(user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            for _ in Session.select().limit(1).where(Session.user == user):
                raise SessionExists()
            else:
                if user.passwd == user_pass:
                    user.failed_logins = 0
                    user.save()
                    session = Session.start(user)
                    return func(*args, **kwargs), session.token
                else:
                    user.failed_logins += 1
                    user.save()
                    raise InvalidCredentials()

    return _login


def authenticate(func):
    """Authenticate for a method"""
    def _authenticate(*args, user_name=None, session_token=None, **kwargs):
        """Refresh a session for a user"""
        if user_name is None or session_token is None:
            raise NotAuthenticated()
        user = User.by_hashed_name(user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    session = session.refresh()
                    return func(*args, **kwargs), session.token
                else:
                    session.terminate()
                    raise SessionTimeout()
            else:
                raise NotLoggedIn()

    return _authenticate


def authorize(func):
    """Adds authorization to a method"""
    def _authorize_group(group, service):
        """Determines whether a user is allowed to access a certain resource"""
        for _ in (GroupService.select()
                  .where(GroupService.group == group
                         and GroupService.service == service)):
            return True
        else:
            raise UnauthorizedGroup()

    def _authorize(*args, user_name=None, service_name=None, **kwargs):
        """Determines whether a user is allowed to access a certain resource"""
        if user_name is None or service_name is None:
            raise NotAuthorized()
        user = User.by_hashed_name(user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            service = Service.by_name(service_name)
            if service is None:
                raise NoSuchService()
            elif _authorize_group(user.group, service):
                for _ in (UserService.select()
                          .where(UserService.user == user
                                 and UserService.service == service)):
                    return func(*args, **kwargs)
                else:
                    raise UnauthorizedUser()
            else:
                raise UnauthorizedGroup()

    return _authorize
