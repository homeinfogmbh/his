"""
Logging for HIS
"""


class _Error():
    """
    An error class
    """
    def __init__(self, code, msg, desc):
        """Initialize code and description"""
        self.__code = code
        self.__msg = msg
        self.__desc = desc

    @property
    def code(self):
        """Returns the error code"""
        return self.__code

    @property
    def msg(self):
        """Returns the error message"""

    @property
    def desc(self):
        """Returns the error description"""
        return self.__desc


class Error():
    """
    Error codes
    """
    NOT_AUTHENTICATED = 1
    INVALID_CREDENTIALS = 2
    SESSION_TIMED_OUT = 3
    UNAUTHORIZED = 4
    NO_SUCH_SERVICE = 5


class Logger():
    """
    A logger
    """
    pass
