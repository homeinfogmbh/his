"""
Database configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['deferred_db', 'HISModel']

from peewee import Model
from ..config import deferred_db

class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = deferred_db    