"""
Defines the HIS service databases
"""
from .config import db, wsgi
from peewee import MySQLDatabase
from os.path import join

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase', 'Service']


class HISServiceDatabase(MySQLDatabase):
    """A HIS service database"""
    def __init__(self, service, host=None, user=None,
                 passwd=None, threadlocals=False, **kwargs):
        if host is None:
            host = db.get('host')
        if user is None:
            user = db.get('user')
        if passwd is None:
            passwd = db.get('passwd')
        """Changes the name to create a '_'-separated namespace"""
        super().__init__('_'.join([db.get('master_db'), str(service)]),
                         host=host, user=user, passwd=passwd,
                         threadlocals=threadlocals, **kwargs)


class Service():
    """Common service class"""
    @property
    def name(self):
        """Returns the service's name"""
        return self.__class__.__name__

    @property
    def root(self):
        """Returns the service's root path"""
        return join(wsgi.get('root'), self.name.lower())
