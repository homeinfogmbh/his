"""
Service definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Service']

from .abc import Resource
from peewee import TextField, CharField

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