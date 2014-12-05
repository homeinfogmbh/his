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
            # User with specified name has
            # not been found in the database
            raise InvalidCredentials()
        elif user.locked:
            # User is marked as locked
            raise UserLocked()
        elif user.passwd == user_pass:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    # An active session has been found
                    # and double login is not allowed
                    raise SessionExists()
                else:
                    # A time-outed session has been found
                    # so just remove it
                    session.terminate()
            else:
                # No active session have been found
                # so start a new one
                session = Session.start(user)
                # Reset failed logins to zero
                # after successful login
                user.failed_logins = 0
                user.save()
                result = func(*args, **kwargs)
                result.session_token = session.token
                return result
        else:
            # User has provided an invalid password
            # so raise amount of failed logins
            user.failed_logins += 1
            user.save()
            raise InvalidCredentials()

    def _session(user_name, session_token, *args, **kwargs):
        """Refresh a session for a user"""
        user = User.by_user_name(user_name)
        if user is None:
            # User with specified name has
            # not been found in the database
            raise InvalidCredentials()
        elif user.locked:
            # User is marked as locked
            raise UserLocked()
        else:
            for session in Session.select().limit(1).where(Session.user
                                                           == user):
                if session.valid:
                    # A valid session has been found
                    if session.token == session_token:
                        # Session token matches, so refresh session
                        session = session.refresh()
                        result = func(*args, **kwargs)
                        result.session_token = session.token
                        return result
                    else:
                        # The session token is invalid
                        # Does somebody try to intrude?
                        raise InvalidCredentials()
                else:
                    # The session has timed out
                    # So terminate it an raise appropriate error
                    session.terminate()
                    raise SessionTimeout()
            else:
                # There is no session for the user
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
                    return _login(user_name, user_pass, *args, **kwargs)
            else:
                if user_pass is None:
                    return _session(user_name, session_token,
                                    *args, **kwargs)
                else:
                    raise InvalidCredentials()

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
