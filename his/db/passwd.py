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
    def admins(self):
        """Fetches all admins of the group"""
        for member in self.members:
            if member.admin:
                yield member


class User(HISModel):
    """
    A HOMEINFO Integrated Services user
    """
    email = CharField(64)
    """A unique email address"""
    first_name = CharField(32, null=True)
    """The user's first name"""
    last_name = CharField(32, null=True)
    """The user's last name"""
    _passwd = CharField(69, db_column='passwd')
    """The user's SHA-512 encrypted login password"""
    group = ForeignKeyField(Group, db_column='group', related_name='members')
    """The primary group of the user"""
    admin = BooleanField()
    """Flag, whether the user is an administrator"""
    last_login = DateTimeField(null=True)
    """Date and time of the last login"""
    failed_logins = IntegerField()
    """Number of failed login attempts"""
    disabled = BooleanField()
    """Flag to disable the user for login"""

    @property
    def name(self):
        """Returns the user's name"""
        return self.email

    @name.setter
    def name(self, name):
        """Sets the user's name"""
        self.email = name

    @property
    def passwd(self):
        """Returns the password"""
        return self._passwd

    @passwd.setter
    def passwd(self, passwd):
        """Encrypts and sets the password"""
        self._passwd = str(sha256(passwd.encode()).hexdigest())

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
        return str(sha256(self.name.encode()).hexdigest())

    @property
    def superadmin(self):
        """Determines whether the user is a super-administrator"""
        if self.admin and self.group.customer.id == 1000:
            return True
        else:
            return False

    @classmethod
    def by_id(cls, ident):
        """Returns a user by its ID"""
        for user in cls.select().limit(1).where(cls.id == ident):
            return user

    @classmethod
    def by_name(cls, name):
        """Returns a user by its ID"""
        for user in cls.select().limit(1).where(cls.name == name):
            return user

    @classmethod
    def by_hashed_name(cls, sha256name):
        """Returns a user by its hashed name"""
        for user in cls.select().where(True):
            if str(sha256(user.name.encode()).hexdigest()) == sha256name:
                return user

    @classmethod
    def admins(cls):
        """Returns all administrators"""
        return cls.select().where(cls.admin == 1)

    @classmethod
    def superadmins(cls):
        """Returns all super-administrators"""
        return cls.select().where(cls.superadmin is True)
