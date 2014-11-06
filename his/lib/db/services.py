"""
Service definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Service', 'UserServices', 'GroupServices']

from .abc import HISModel
from .passwd import User, Group
from peewee import CharField, ForeignKeyField

class Service(HISModel):
    """
    A HIS-service
    """
    name = CharField(16)
    """A representative name"""
    description = CharField(256)
    """A description of the service"""
    
    
class UserService(HISModel):
    """
    Many-to-many mapping for users and services
    """
    user = ForeignKeyField(User, related_name='services')
    service = ForeignKeyField(Service, related_name='users')
    
    
class GroupService(HISModel):
    """
    Many-to-many mapping for groups and services
    """
    group = ForeignKeyField(Group, related_name='services')
    service = ForeignKeyField(Service, related_name='groups')