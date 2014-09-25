"""
Database configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['deferred_db', 'CreamModel']

from peewee import MySQLDatabase, Model

deferred_db = MySQLDatabase(None)

class CreamModel(Model):
    """
    Generic CREAM-DB model
    """
    class Meta:
        database = deferred_db    