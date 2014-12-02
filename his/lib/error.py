"""
Handles service access
"""
from pcp import pcp

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['InvalidCredentialsError', 'SessionTimeoutError',
           'SessionExistsError']


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

    def __render__(self):
        """Renders itself as a PCP message to bytes"""
        return self.__pcp__().toxml(encoding='utf-8')

    def __str__(self):
        """Converts the message to a PCP Message XML string"""
        return self.__render__().decode()


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
