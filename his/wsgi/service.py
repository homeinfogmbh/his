"""
Handles service access
"""
from .session import SessionController
from homeinfo.his.db import UserService, GroupService

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['GroupServiceController', 'SessionController']


class GroupServiceController():
    """
    Handles resources
    """
    @classmethod
    def allowed(cls, group, service):
        """Determines whether a user is allowed to access a certain resource"""
        for group_service in (GroupService.select()
                              .where(GroupService.group == group)):
            if group_service.service == service:
                return True
        return False


class UserServiceController():
    """
    Handles resources
    """
    @classmethod
    def allowed(cls, user, service):
        """Determines whether a user is allowed to access a certain resource"""
        if SessionController.active(user):
            for user_service in (UserService.select()
                                 .where(UserService.user == user)):
                if user_service.service == service:
                    if GroupServiceController.is_allowed(user.group, service):
                        return True
        return False
