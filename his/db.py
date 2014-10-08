"""
Basic HIS database definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '08.10.2014'

__all__ = ['HISModel']

from peewee import MySQLDatabase, Model

db = MySQLDatabase()

class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = db