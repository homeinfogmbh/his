"""Group and user definitions"""

from .abc import HISModel
from homeinfo.crm import Customer
from peewee import (ForeignKeyField, CharField, BooleanField,
                    DateTimeField, IntegerField)
from hashlib import sha256
from datetime import datetime, timedelta

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'
__all__ = ['Group', 'User']


class Account(HISModel):
    """A HIS account"""

    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='his_accounts')
    """The respective customer who owns this account"""
    created = DateTimeField(default=datetime.now())
    """The date and time when the account was created"""
    deleted = DateTimeField(null=True)
    """The date and time when the account was deleted"""
    locked = BooleanField(default=False)
    """Flag whether the account has been locked"""


class Service(HISModel):
    """Registers services of HIS"""

    name = CharField(32)
    """A unique name for the service"""


class AccountServices(HISModel):
    """Many-to-many Account <-> Services mapping"""

    account = ForeignKeyField(Account, db_column='account',
                              related_name='_account_services')
    """The respective account"""
    service = ForeignKeyField(Service, db_column='service',
                              related_name='_service_accounts')
    """The respective service"""


class Login(HISModel):
    """A HIS login account"""

    name = CharField(64)
    """The login name"""
    passwd = CharField(64)
    """The SHA-256 hash of the password"""
    email = CharField(64)
    """A unique email address"""
    account = ForeignKeyField(Account, db_column='account',
                              related_name='logins')
    """The account this login belongs to"""
    user = ForeignKeyField(User, db_column='user', related_name='logins')
    """The respective user data for this login"""
    created = DateTimeField(default=datetime.now())
    """The date and time when the login was created"""
    deleted = DateTimeField(null=True)
    """The date and time when the login was deleted"""
    last_login = DateTimeField(null=True)
    """Date and time of the last login"""
    failed_logins = IntegerField()
    """Number of failed login attempts since last successful login"""
    locked_until = DateTimeField(null=True, default=None)
    """Login is locked until date"""
    disabled = BooleanField(default=True)
    """Flag to disable the user for login"""
    admin = BooleanField(default=False)
    """Flag, whether the user is an administrator
    of the respective account
    """
    root = BooleanField(default=False)
    """Flag, whether the user is an super-admin of the system
    XXX: This login can do ANYTHING!"""

    @property
    def password(self):
        """Returns the cleartext password"""
        raise SecurityError('Cannot return clear text password')

    @passwd.setter
    def passwd(self, passwd):
        """Encrypts and sets the password"""
        self._passwd = str(sha256(passwd.encode()).hexdigest())

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if self.locked_until is None:
            if self.disabled or self.failed_logins >= 3:
                return True
            else:
                return False
        else:
            if self.locked_until - datetime.now() > timedelta(seconds=0):
                return True
            else:
                return False

    @property
    def user_name(self):
        """Returns the SHA-256 encoded email"""
        return str(sha256(self.email.encode()).hexdigest())

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
    def by_email(cls, email):
        """Returns a user by its ID"""
        for user in cls.select().limit(1).where(cls.email == email):
            return user

    @classmethod
    def by_user_name(cls, user_name):
        """Returns a user by its hashed name"""
        for user in cls.select().where(True):
            if user.user_name == user_name:
                return user

    @classmethod
    def admins(cls):
        """Returns all administrators"""
        return cls.select().where(cls.admin)

    @classmethod
    def superadmins(cls):
        """Returns all super-administrators"""
        for user in cls.select().where(True):
            if user.superadmin:
                yield user


class User(HISModel):
    """User data"""

    salutation = CharField(8, null=True)
    """The salutation of the person"""
    first_name = CharField(32, null=True)
    """The user's first name"""
    last_name = CharField(32, null=True)
    """The user's last name"""

    @property
    def name(self):
        """Returns the user's name"""
        if self.first_name is None:
            if self.last_name is None:
                return None
            else:
                if self.salutation is None:
                    return self.last_name
                else:
                    ' '.join([self.salutation, self.last_name])
        else:
            if self.last_name is None:
                return self.first_name
            else:
                if self.salutation is None:
                    return ' '.join([self.first_name, self.last_name])
                else:
                    return ' '.join([self.salutation, self.first_name,
                                     self.last_name])
