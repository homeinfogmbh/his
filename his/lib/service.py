"""
Handles service access
"""
from .session import SessionHandler
from homeinfo.his.db import Service

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'


class ServiceHandler():
    """
    Handles resources
    """
    @classmethod
    def allowed(cls, user, service):
        """Determines whether a user is allowed to access a certain resource"""
        if SessionHandler.logged_in(user):
            for service in Service.select().where(Service.user == user):
                return True
        return False
