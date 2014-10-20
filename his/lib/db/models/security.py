'''
Created on 09.10.2014

@author: neumannr
'''
from .abc import HISModel
from .passwd import User
from peewee import ForeignKeyField, BooleanField, TextField

class Permissions(HISModel):
    """
    Table that assigns permissions for users on resources
    """
    user = ForeignKeyField(User, related_name='permissions')
    """The user, this permissions apply to"""
    create = BooleanField()
    """Allow to create instances of the targeted resource"""
    retrieve = BooleanField()
    """Allow to retrieve instances of the targeted resource"""
    update = BooleanField()
    """Allow to update instances of the targeted resource"""
    delete = BooleanField()
    """Allow to delete instances of the targeted resource"""
    resource = TextField()
    """The name of the targeted resource"""