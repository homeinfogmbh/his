"""
Permissions definition tables
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Resource', 'UserPermissions', 'GroupPermissions']

from .abc import HISModel
from .passwd import User, Group
from peewee import ForeignKeyField, BooleanField, CharField, DateTimeField,\
    IntegerField

class _Permissions(HISModel):
    """
    Abstract, basic permissions definition
    """
    create = BooleanField()
    """Allow to create instances of the targeted resource"""
    retrieve = BooleanField()
    """Allow to retrieve instances of the targeted resource"""
    update = BooleanField()
    """Allow to update instances of the targeted resource"""
    delete = BooleanField()
    """Allow to delete instances of the targeted resource"""
    
        
class Resource(HISModel):
    """
    Resource on which permissions can be applied
    """
    uuid = CharField(36)
    """Universally unique identifier"""
    table = CharField(36)
    """The name of the appropriate resource's table"""
    record = IntegerField()
    """The record's identifier inside the respective table"""
    created = DateTimeField()
    """Date of creation"""
    retrieved = DateTimeField()
    """Date of last access"""
    updated = DateTimeField()
    """Date of last update"""
    deleted = DateTimeField()
    """Date of deletion"""
    delete = BooleanField()
    """Flag for deletion"""
    
    
class UserPermissions(_Permissions):
    """
    Model that assigns permissions on a resource to a user
    """
    user = ForeignKeyField(User, related_name='permissions')
    """The user, this permissions apply to"""
    resource = ForeignKeyField(Resource, related_name='user_permissions')
    """The resource, this permissions apply to"""
    
    
class GroupPermissions(_Permissions):
    """
    Model that assigns permissions on a resource to a group
    """
    group = ForeignKeyField(Group, related_name='permissions')
    """The group, this permissions apply to"""
    resource = ForeignKeyField(Resource, related_name='group_permissions')
    """The resource, this permissions apply to"""