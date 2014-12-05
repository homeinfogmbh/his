"""
Handles service access
"""
from .db import Service, UserService, GroupService, User, Session
from .lib.error import *

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '04.12.2014'
__all__ = ['authenticate', 'authorize']


def authenticate(func):
    """Authenticate for a method"""
    def _login(user_name, user_pass, *args, **kwargs):
        """Create a session for a user"""
        user = User.by_user_name(user_name)
        if user is None:
            raise InvalidCredentials()
        elif user.locked:
            raise UserLocked()
        elif user.passwd == user_pass:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    raise SessionExists()
                else:
                    session.terminate()
            else:
                session = Session.start(user)
                user.failed_logins = 0
                user.save()
                result = func(*args, **kwargs)
                result.session_token = session.token
                return result
        else:
            user.failed_logins += 1
            user.save()
            raise InvalidCredentials()

    def _session(user_name, session_token, *args, **kwargs):
        """Refresh a session for a user"""
        user = User.by_user_name(user_name)
        if user is None:
            raise InvalidCredentials()
        elif user.locked:
            raise UserLocked()
        else:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    if session.token == session_token:
                        session = session.refresh()
                        result = func(*args, **kwargs)
                        result.session_token = session.token
                        return result
                    else:
                        raise InvalidCredentials()
                else:
                    session.terminate()
                    raise SessionTimeout()
            else:
                raise NotLoggedIn()

    def authenticate(*args, user_name=None, session_token=None,
                     user_pass=None, **kwargs):
        """Authenticate the user via active session or login"""
        if user_name is None:
            raise NotAuthenticated()
        else:
            if session_token is None:
                if user_pass is None:
                    raise InvalidCredentials()
                else:
                    return _login(*args, user_name=user_name,
                                  user_pass=user_pass, **kwargs)
            else:
                return _session(*args, user_name=user_name,
                                session_token=session_token, **kwargs)

    return authenticate


def authorize(func):
    """Adds authorization to a method"""
    def authorize_group(group, service):
        """Determines whether a user is allowed to access a certain resource"""
        for _ in (GroupService.select()
                  .where(GroupService.group == group
                         and GroupService.service == service)):
            return True
        else:
            raise UnauthorizedGroup()

    def authorize(*args, user_name=None, service_name=None, **kwargs):
        """Determines whether a user is allowed to access a certain resource"""
        if user_name is None or service_name is None:
            raise NotAuthorized()
        user = User.by_user_name(user_name)
        if user is None:
            raise InvalidCredentials()
        elif user.locked:
            raise UserLocked()
        else:
            service = Service.by_name(service_name)
            if service is None:
                raise NoSuchService()
            elif authorize_group(user.group, service):
                for _ in (UserService.select()
                          .where(UserService.user == user
                                 and UserService.service == service)):
                    return func(*args, **kwargs)
                else:
                    raise UnauthorizedUser()
            else:
                raise UnauthorizedGroup()

    return authorize
