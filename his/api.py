"""
Defines the HIS service databases
"""
from his.config import db
from playhouse.pool import PooledMySQLDatabase

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase']


class HISServiceDatabase(PooledMySQLDatabase):
    """A HIS service database"""
    def __init__(self, database, host=None, user=None,
                 passwd=None, threadlocals=True, **kwargs):
        if host is None:
            host = db.get('host')
        if user is None:
            user = db.get('user')
        if passwd is None:
            passwd = db.get('passwd')
        """Changes the name to create a '_'-separated namespace"""
        super().__init__('_'.join([db.get('master_db'), database]),
                         host=host, user=user, passwd=passwd,
                         threadlocals=threadlocals, kwargs)
