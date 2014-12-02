"""
Handles service access
"""
from pcp import pcp

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'


class PcpError(Exception):
    """
    An error that can be rendered as a PCP exception
    """
    def __init__(self, msg, code):
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

    def __render__(self):
        """Determines whether a user is allowed to access a certain resource"""
        msg = pcp.ErrorMessage()
        msg.code = self.code
        msg.msg = self.msg
        return msg.toxml(encoding='utf-8')
