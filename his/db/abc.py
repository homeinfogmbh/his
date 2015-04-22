"""Basic HIS database definitions"""

from peewee import Model, MySQLDatabase
from ..config import db

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['HISModel']


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model"""
    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('HOST'),
                                 user=db.get('USER'),
                                 passwd=db.get('PASSWD'),
                                 threadlocals=True)
        schema = database.database
