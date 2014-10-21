"""
Basic HIS database definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['HISModel', 'Resource']

from peewee import Model
from ..config import database

class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = database