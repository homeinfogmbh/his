"""
Basic HIS database definitions
"""
from ..config import db
from peewee import Model, MySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['HISModel']


class HISModel(Model):
    """
    Generic HOMEINFO Integrated Service database model
    """
    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('HOST'),
                                 user=db.get('USER'),
                                 passwd=db.get('PASSWD'),
                                 threadlocals=True)

    def __enter__(self):
        """Open a connection explicitly"""
        self._meta.database.connect()
        return self

    def __exit__(self, tpe, value, tb):
        """Closes a connection if existent"""
        try:
            self._meta.database.close()
        except:
            pass
