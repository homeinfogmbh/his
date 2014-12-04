"""
Handles service access
"""
import pcp

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['InvalidCredentialsError', 'SessionTimeoutError',
           'SessionExistsError', 'NoSuchUser', 'UserLocked', 'NotLoggedIn',
           'NoSuchService', 'UnauthorizedUser', 'UnauthorizedGroup']


class Message(Exception):
    """
    An error that can be rendered as a PCP exception
    """
    def __init__(self, code, msg):
        """Initializes with a code and a message"""
        self.__code = code
        self.__msg = msg

    @property
    def code(self):
        """Returns the error code"""
        return self.__code

    @property
    def msg(self):
        """Returns the error message"""
        return self.__msg

    def __pcp__(self):
        """Converts the message to a PCP Message"""
        rsp = pcp.rsp()
        msg = pcp.Message()
        msg.code = self.code
        msg.msg = self.msg
        rsp.msg = msg
        return rsp

    def __xml__(self):
        """Renders itself as a PCP message to XML bytes"""
        return self.__pcp__().toxml(encoding='utf-8')

    def __json__(self):
        """Renders itself as a PCP message to JSON bytes"""
        return self.__pcp__().tojson(encoding='utf-8')

    def __int__(self):
        """Returns the error code number"""
        return self.code

    def __str__(self):
        """Converts the message to a PCP Message XML string"""
        return self.__xml__().decode()

    def __eq__(self, other):
        """Equality comparison"""
        return int(self) == int(other)

    def __gt__(self, other):
        """Greater-than comparison"""
        return int(self) > int(other)

    def __ge__(self, other):
        """Greater-than comparison"""
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        """Greater-than comparison"""
        return int(self) < int(other)

    def __le__(self, other):
        """Greater-than comparison"""
        return self.__lt__(other) or self.__eq__(other)


class InvalidCredentialsError(Message):
    """Indicates that a user tried to log in with invalid credentials"""
    def __init__(self):
        super().__init__(1, 'INVALID_CREDENTIALS')


class SessionTimeoutError(Message):
    """Indicates that a user's session has times out"""
    def __init__(self):
        super().__init__(2, 'SESSION_TIMED_OUT')


class SessionExistsError(Message):
    """Indicates that a session for a user is already running"""
    def __init__(self):
        super().__init__(3, 'SESSION_EXISTS')


class NoSuchUser(Message):
    """Indicates that there is no such user"""
    def __init__(self):
        super().__init__(4, 'NO_SUCH_USER')


class UserLocked(Message):
    """Indicates that a user has been locked"""
    def __init__(self):
        super().__init__(5, 'USER_LOCKED')


class NotLoggedIn(Message):
    """Indicates that a user has no active session"""
    def __init__(self):
        super().__init__(6, 'NOT_LOGGED_IN')


class NoSuchService (Message):
    """Indicates that a service does not exist"""
    def __init__(self):
        super().__init__(7, 'NO_SUCH_SERVICE')


class UnauthorizedUser (Message):
    """Indicates that a user is not allowed to access a service"""
    def __init__(self):
        super().__init__(8, 'UNAUTHORIZED_USER')


class UnauthorizedGroup (Message):
    """Indicates that a user is not allowed to access a service"""
    def __init__(self):
        super().__init__(9, 'UNAUTHORIZED_GROUP')
