"""
Basic HIS database definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['HISModel', 'Resource']

from peewee import Model, CharField, DateTimeField, BooleanField
from ..config import database

class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = database
        
        
class Resource(HISModel):
    """
    Generic, abstract resource on which permission can be applied
    """
    uuid = CharField(36)
    """Universally unique identifier"""
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