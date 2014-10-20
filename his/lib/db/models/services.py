"""
Service definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Service', 'UserServices', 'GroupServices']

from .abc import Resource, HISModel
from .passwd import User, Group
from peewee import TextField, CharField, ForeignKeyField

class Service(Resource):
    """
    A HIS-service
    """
    name = TextField()
    """A representative name"""
    description = TextField()
    """A description of the service"""
    uuid = CharField(36)
    """A universally unique identifier"""
    
    
class UserServices(HISModel):
    """
    Many-to-many mapping for users and services
    """
    user = ForeignKeyField(User, related_name='services')
    service = ForeignKeyField(Service, related_name='users')
    
    
class GroupServices(HISModel):
    """
    Many-to-many mapping for groups and services
    """
    group = ForeignKeyField(Group, related_name='services')
    service = ForeignKeyField(Service, related_name='groups')