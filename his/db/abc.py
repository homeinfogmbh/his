"""
Basic HIS database definitions
"""
from his.config import db
from peewee import Model, MySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['HISModel']


class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = MySQLDatabase('his', host=db.get('HOST'),
                                 user=db.get('USER'),
                                 passwd=db.get('PASSWD'))
