"""Group and user definitions"""

from peewee import Model, MySQLDatabase, PrimaryKeyField, ForeignKeyField,\
    CharField, BooleanField, DateTimeField, IntegerField
from hashlib import sha256
from datetime import datetime, timedelta
from homeinfo.misc import classproperty
from homeinfo.crm.customer import Customer
from homeinfo.crm.company import Employee
from .lib.error.internal import SecurityError
from .config import db

__all__ = ['HISServiceDatabase', 'HISModel', 'Account', 'Service',
           'AccountServices', 'User', 'Login']


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


class Service(HISModel):
    """Registers services of HIS"""

    name = CharField(32)
    advertise = BooleanField(default=True)

    def __repr__(self):
        """Returns the service's ID as a string"""
        return str(self.id)

    def __str__(self):
        """Returns the service's name"""
        return self.name


class CustomerServices(HISModel):
    """Many-to-many Account <-> Services mapping"""

    customer = ForeignKeyField(Customer, db_column='account',
                               related_name='customer_services')
    """The respective account"""
    service = ForeignKeyField(Service, db_column='service',
                              related_name='service_customers')
    """The respective service"""


class Account(HISModel):
    """A HIS login account"""

    name = CharField(64)
    passwd = CharField(64)  # SHA-256 hash
    email = CharField(64)
    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='accounts')
    user = ForeignKeyField(Employee, db_column='user', null=True,
                           related_name='accounts')
    created = DateTimeField()
    deleted = DateTimeField(null=True)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField()
    locked_until = DateTimeField(null=True, default=None)
    disabled = BooleanField(default=True)
    # Flag, whether the user is an administrator of the respective account
    admin = BooleanField(default=False)
    # Flag, whether the user is a super-admin of the system
    # XXX: This login can do ANYTHING!
    root = BooleanField(default=False)

    def __int__(self):
        """Returns the login's ID"""
        return self.id

    def __repr__(self):
        """Returns the login's name"""
        return self.name

    def __bool__(self):
        """Returns whether the user is locked (False) or unlocked (True)"""
        return not self.locked

    @classproperty
    @classmethod
    def admins(cls):
        """Returns all administrators"""
        return cls.select().where(cls.admin)

    @classproperty
    @classmethod
    def superadmins(cls):
        """Returns all super-administrators"""
        return cls.select().where(cls.root)

    @property
    def password(self):
        """Returns the clear text password"""
        raise SecurityError('Cannot return clear text password')

    @password.setter
    def password(self, password):
        """Encrypts a clear text password and
        sets it as the user's password
        """
        self._passwd = str(sha256(password.encode()).hexdigest())

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if self.deleted is None:
            if self.locked_until is None:
                return self.disabled
            else:
                return self.locked_until - datetime.now() > timedelta(0)
        else:
            return False


class Session(HISModel):
    """A session related to a login"""

    account = ForeignKeyField(Account, db_column='login')
    token = CharField(64)   # A uuid4
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField()  # Login session or keep-alive?

    @property
    def valid(self):
        """Determines whether the session is (still) valid"""
        return datetime.now() - self.end > timedelta(0)

    def __bool__(self):
        """Returns a boolean representation"""
        return self.valid

    def __repr__(self):
        """Returns a unique string representation"""
        return self.token

    def __str__(self):
        """Returns a human-readable representation"""
        return ' '.join([': '.join([' - '.join([str(self.start),
                                                str(self.end)]),
                                    repr(self)]),
                         ''.join(['(', str(self.login), ')'])])
