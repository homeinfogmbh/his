"""
Models for simple token authentication
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'

from his.db import HISModel
from peewee import TextField, CharField

class STAClient(HISModel):
    """
    Simple token authentication clients
    """
    name = TextField()
    """A representative name"""
    uuid = CharField(36)
    """A universally unique identifier"""