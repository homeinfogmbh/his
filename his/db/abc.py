"""
Basic HIS database definitions
"""
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['HISModel']

DB = 'homeinfo_his'
HOST = 'mysql.homeinfo.de'
USER = 'homeinfo_his'
PASSWD = '3=w,&7>_u8}oO0y'


class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = PooledMySQLDatabase('his', host=HOST,
                                       user=USER, passwd=PASSWD)
