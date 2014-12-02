"""
Group and user definitions
"""
from .abc import HISModel
from homeinfo.crm import Customer
from peewee import ForeignKeyField, CharField, BooleanField, DateTimeField,\
    IntegerField
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
    passwd = CharField(128, db_column='passwd')
    """The user's SHA-512 encrypted login password"""
    group = ForeignKeyField(Group, db_column='group')
    """The primary group of the user"""
    admin = BooleanField()
    """Flag, whether the user is an administrator"""
    last_login = DateTimeField()
    """Date and time of the last login"""
    failed_logins = IntegerField()
    """Number of failed login attempts"""
    disabled = BooleanField()
    """Flag to disable the user for login"""

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if self.disabled or self.failed_logins >= 3:
            return True
        else:
            return False

    @property
    def hashed_name(self):
        """Returns the SHA-256 encoded name"""
        return str(sha256(self.name.encode()))

    @property
    def root(self):
        """Determines whether the user is a super-user aka. root"""
        if self.admin and self.group.customer.id == 1000:
            return True
