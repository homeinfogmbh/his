"""
Service definitions
"""
from .abc import HISModel
from .passwd import User, Group
from peewee import CharField, ForeignKeyField, BooleanField

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['Service', 'UserServices', 'GroupServices']


class Service(HISModel):
    """
    A HIS-service
    """
    name = CharField(16)
    """A representative name"""
    description = CharField(256)
    """A description of the service"""
    public = BooleanField()
    """Flag whether the service is public
    and thus requires no authentication"""

    @classmethod
    def by_name(cls, name):
        """Fetches a service by its name"""
        for service in cls.select().limit(1).where(cls.name == name):
            return service


class UserService(HISModel):
    """
    Many-to-many mapping for users and services
    """
    user = ForeignKeyField(User, related_name='services', db_column='user')
    service = ForeignKeyField(Service, related_name='users',
                              db_column='service')


class GroupService(HISModel):
    """
    Many-to-many mapping for groups and services
    """
    group = ForeignKeyField(Group, related_name='services', db_column='group')
    service = ForeignKeyField(Service, related_name='groups',
                              db_column='service')
