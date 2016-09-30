"""File management module"""

from peewee import Model, PrimaryKeyField, ForeignKeyField, IntegerField, \
    CharField

from homeinfo.peewee import MySQLDatabase

from his.locale import Language
from his.api.errors import HISMessage
from his.api.handlers import AuthorizedService


class Inode(Model):
    """Inode database model for the virtual filesystem"""

    class Meta:
        database = MySQLDatabase(
            # TODO: configure
            )
        schema = database.database

    id = PrimaryKeyField()
    _name = CharField(255, db_column='name')
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)
    file = IntegerField()   # FileID from FileDB

    @property
    def name(self):
        """Returns the inode's name"""
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name"""
        if not name:
            raise ValueError('File name must not be empty.')
        elif '/' in name:
            raise ValueError('File name must not contain "/".')
        else:
            self._name = name

class FileManager(AuthorizedService):
    """Service that manages files"""

    def get(self):
        """Retrieves information about a file"""
        if self.resource is None:
            # Retrieves all files
            # TODO: implement
            pass
        else:
            file_id = self.resource

            
