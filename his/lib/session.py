"""
Handles requests on services
"""
from homeinfo.his.db import Session

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '21.10.2014'
__all__ = ['SessionHandler']


class SessionHandler():
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
