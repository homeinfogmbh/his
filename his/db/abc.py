"""Basic HIS database definitions"""

from peewee import Model, MySQLDatabase, PrimaryKeyField
from ..config import db

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '24.04.2015'
__all__ = ['HISServiceDatabase', 'HISModel']


class HISServiceDatabase(MySQLDatabase):
    """A HIS service database
    Gets the name of the service, prefixed by the master database
    """

    def __init__(self, service, host=None, user=None, passwd=None, **kwargs):
        """Initializes the database with the respective service's
        name and optional diverging database configuration
        """
        if host is None:
            host = db.get('host')
        if user is None:
            user = db.get('user')
        if passwd is None:
            passwd = db.get('passwd')
        # Change the name to create a '_'-separated namespace
        super().__init__('_'.join([db.get('master_db'), repr(service)]),
                         host=host, user=user, passwd=passwd, **kwargs)


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model"""

    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('HOST'),
                                 user=db.get('USER'),
                                 passwd=db.get('PASSWD'))
        schema = database.database

    id = PrimaryKeyField()
    """The table's primary key"""
