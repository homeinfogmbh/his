"""
Handles service access
"""
from homeinfo.his.db import Service, UserService, GroupService, User
from homeinfo.his.lib.error import (NoSuchUser, UserLocked, NoSuchService,
                                    UnauthorizedUser, UnauthorizedGroup)

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['ServiceController']


class ServiceController():
    """
    Handles resources
    """
    @classmethod
    def access(cls, hashed_user_name, service_name):
        """Determines whether a user is allowed to access a certain resource"""
        user = User.by_hashed_name(hashed_user_name)
        if user is None:
            raise NoSuchUser()
        elif user.locked:
            raise UserLocked()
        else:
            service = Service.by_name(service_name)
            if service is None:
                raise NoSuchService()
            elif cls._group_access(user.group, service):
                for _ in (UserService.select()
                          .where(UserService.user == user
                                 and UserService.service == service)):
                    return True
                else:
                    raise UnauthorizedUser()
        return False

    @classmethod
    def _group_access(cls, group, service):
        """Determines whether a user is allowed to access a certain resource"""
        for _ in (GroupService.select()
                  .where(GroupService.group == group
                         and GroupService.service == service)):
            return True
        else:
            raise UnauthorizedGroup()
