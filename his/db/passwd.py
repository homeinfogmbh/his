"""
Group and user definitions
"""
from .abc import HISModel
from homeinfo.crm import Customer
from peewee import ForeignKeyField, CharField
from hashlib import sha256

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['Group', 'User', 'GroupMembers']


class Group(HISModel):
    """
    A HOMEINFO Integrated Services group
    """
    customer = ForeignKeyField(Customer, db_column='customer')
    """Customer identifier of the corresponding customer"""
    name = CharField(64)
    """A representative name"""
    @property
    def members(self):
        """Fetch all users that are in this group"""
        return (User.select().where(User.group == self))


class User(HISModel):
    """
    A HOMEINFO Integrated Services user
    """
    name = CharField(64)
    """A representative name"""
    sha512passwd = CharField(128)
    """The user's encrypted login password"""
    group = ForeignKeyField(Group, db_column='group')
    """The primary group of the user"""

    @property
    def sha256name(self):
        """Returns the SHA-256 encoded name"""
        return str(sha256(self.name.encode()))

    @property
    def passwd(self):
        """Returns the user's password"""
        return self.sha512passwd

    @passwd.setter
    def passwd(self, passwd):
        """Sets the password"""
        self.sha512passwd = passwd
