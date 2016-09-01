"""Group and user definitions"""

from os.path import dirname
from datetime import datetime, timedelta
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from peewee import Model, PrimaryKeyField, ForeignKeyField,\
    CharField, BooleanField, DateTimeField, IntegerField, DoesNotExist

from homeinfo.lib.misc import classproperty
from homeinfo.peewee import MySQLDatabase
from homeinfo.crm import Customer, Employee

from his.api.errors import InvalidCredentials, AlreadyLoggedIn
from his.config import config

__all__ = [
    'his_db',
    'AlreadyLoggedIn',
    'HISServiceDatabase',
    'HISModel',
    'Service',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'tables']


his_db = MySQLDatabase(
    config.db['db'],
    host=config.db['HOST'],
    user=config.db['USER'],
    passwd=config.db['PASSWD'],
    closing=True)


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration"""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


def check_service_consistency(customer=None):
    """Check service assignment consistency"""

    pass  # TODO: Implement


class AccountServicesWrapper():
    """Wraps service mappings with manipulation options"""

    def __init__(self, account):
        self.account = account

    def __iter__(self):
        for account_service in AccountService.select().where(
                AccountService.account == self.account):
            yield account_service.service

    def add(self, service):
        """Adds a service to the mapping"""
        if service not in self:
            if service in CustomerService.services(self.account.customer):
                account_service = AccountService()
                account_service.account = self.account
                account_service.service = service
                return account_service.save()
            else:
                raise InconsistencyError(
                    'Cannot enable service {0} for account {1}, '
                    'because the respective customer {2} is not '
                    'enabled for it'.format(
                        service, self.account, self.account.customer))

    def remove(self, service):
        """Removes a service from the mapping"""
        for account_service in AccountService.select().where(
                (AccountService.account == self.account) &
                (AccountService.service == service)):
            account_service.delete_instance()


class HISServiceDatabase(MySQLDatabase):
    """A HIS service database
    Gets the name of the service, prefixed by the master database
    """

    def __init__(self, service, host=None, user=None, passwd=None, **kwargs):
        """Initializes the database with the respective service's
        name and optional diverging database configuration
        """
        if host is None:
            host = config.db['host']

        if user is None:
            user = config.db['user']

        if passwd is None:
            passwd = config.db['passwd']

        # Change the name to create a '_'-separated namespace
        super().__init__(
            '_'.join((config.db['db'], str(service).lower())),
            host=host, user=user, passwd=passwd, closing=True, **kwargs)


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model"""

    class Meta:
        database = his_db
        schema = database.database

    id = PrimaryKeyField()


class Service(HISModel):
    """Registers services of HIS"""

    path = CharField(255)
    module = CharField(255)
    handler = CharField(32)
    name = CharField(32, null=True, default=None)
    description = CharField(255, null=True, default=None)
    # Flag whether the service shall be promoted
    promote = BooleanField(default=True)

    def __repr__(self):
        """Returns the service's ID as a string"""
        return '.'.join(self.module, self.handler)

    def __str__(self):
        """Returns the service's name"""
        return self.name

    @classmethod
    def by_relpath(cls, relpath):
        """Returns the best matching service
        for the relative URL path
        """
        while relpath:
            try:
                return cls.get(cls.path == relpath)
            except DoesNotExist:
                relpath = dirname(relpath)

        raise DoesNotExist('No handler found for path {}'.format(relpath))


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping"""

    class Meta:
        db_table = 'customer_service'

    customer = ForeignKeyField(
        Customer, db_column='account',
        related_name='customer_services')
    service = ForeignKeyField(
        Service, db_column='service',
        related_name='service_customers')
    begin = DateTimeField(null=True, default=None)
    end = DateTimeField(null=True, default=None)

    def remove(self):
        """Safely removes a customer service and its dependencies"""
        for account_service in AccountService.select().where(
                (AccountService.account.customer == self.customer) &
                (AccountService.service == self.service)):
            account_service.delete_instance()

    @classmethod
    def services(cls, customer):
        """Yields services for the respective customer"""
        for customer_service in cls.select().where(cls.customer == customer):
            yield customer_service.service

    @property
    def active(self):
        """Determines whether the service mapping is active"""
        if self.begin is None:
            if self.end is None:
                return True
            else:
                return datetime.now() < self.end
        else:
            if self.end is None:
                return datetime.now() >= self.begin
            else:
                return self.begin <= datetime.now() < self.end


class Account(HISModel):
    """A HIS login account"""

    _PASSWORD_HASHER = PasswordHasher()

    customer = ForeignKeyField(
        Customer, db_column='customer',
        related_name='accounts')
    user = ForeignKeyField(
        Employee, db_column='user', null=True,
        related_name='accounts')
    name = CharField(64)  # Login name
    pwhash = CharField(73)  # Argon2 hash
    email = CharField(64)
    created = DateTimeField()
    deleted = DateTimeField(null=True, default=None)
    last_login = DateTimeField(null=True, default=None)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True, default=None)
    disabled = BooleanField(default=True)
    # Flag, whether the account is an
    # administrator of the respective customer
    admin = BooleanField(default=False)
    # Flag, whether the user is a super-admin of the system
    # XXX: Such accounts can do ANYTHING!
    root = BooleanField(default=False)

    def __int__(self):
        """Returns the login's ID"""
        return self.id

    def __repr__(self):
        """Returns the login name"""
        return self.name

    def __str__(self):
        """Returns the login name and appropriate customer"""
        return '{0}@{1}'.format(repr(self), repr(self.customer))

    def __bool__(self):
        """Returns whether the user is not locked"""
        return not self.locked

    @classproperty
    @classmethod
    def superadmins(cls):
        """Returns all super-administrators"""
        return cls.select().where(cls.root == 1)

    @classmethod
    def admins(cls, customer=None):
        """Yields administrators"""
        if customer is None:
            return cls.select().where(cls.admin == 1)
        else:
            return cls.select().where(
                (cls.customer == customer) &
                (cls.admin == 1))

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if not self.passwd:
            return True
        elif self.deleted:
            return True
        elif self.disabled:
            return True
        elif self.locked_until > datetime.now():
            return True
        else:
            return False

    @property
    def services(self):
        """Yields appropriate services"""
        return AccountServicesWrapper(self)

    def login(self, passwd):
        """Performs a login"""
        try:
            match = self._PASSWORD_HASHER.verify(self.pwhash, passwd)
        except VerifyMismatchError:
            raise InvalidCredentials()
        else:
            if match:
                return Session.open(self)
            else:
                raise InvalidCredentials()


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping"""

    class Meta:
        db_table = 'account_service'

    account = ForeignKeyField(Account, db_column='account')
    service = ForeignKeyField(Service, db_column='service')


class Session(HISModel):
    """A session related to a login"""

    DEFAULT_DURATION_MINUTES = 5

    account = ForeignKeyField(Account, db_column='account')
    token = CharField(64)   # A uuid4
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField()  # Login session or keep-alive?

    def __repr__(self):
        """Returns a unique string representation"""
        return self.token

    def __str__(self):
        """Returns a human-readable representation"""
        return ' '.join([': '.join(
            [' - '.join([str(self.start), str(self.end)]), repr(self)]),
            ''.join(['(', str(self.login), ')'])])

    @classmethod
    def exists(cls, account):
        """Determines whether a session
        exists for the specified account
        """
        try:
            cls.get(cls.account == account)
        except DoesNotExist:
            return False
        else:
            return True

    @classmethod
    def _open(cls, account, duration=None):
        """Actually opens a new login session"""
        now = datetime.now()
        duration = duration or timedelta(minutes=cls.DEFAULT_DURATION_MINUTES)
        session = cls()
        session.account = account
        session.token = str(uuid4())
        session.start = now
        session.end = now + duration
        session.login = True
        session.save()
        return session

    @classmethod
    def open(cls, account, duration=None):
        """Opens a login session for the specified account
        XXX: This must only be done after successful login
        """
        try:
            session = cls.get(cls.account == account)
        except DoesNotExist:
            return cls._open(account, duration=duration)
        else:
            if session.active:
                raise AlreadyLoggedIn()
            else:
                session.close()
                return cls._open(account, duration=duration)

    @property
    def active(self):
        """Determines whether the session is active"""
        return self.start <= datetime.now() < self.end

    def reload(self):
        """Re-loads the session information from the database"""
        cls = self.__class__
        return cls.get(
            (cls.account == self.account) &
            (cls.token == self.token) &
            (cls.start == self.start) &
            (cls.end == self.end) &
            (cls.login == self.login))

    def close(self):
        """Closes the session"""
        return self.delete_instance()

    def renew(self, duration=None):
        """Renews the session"""
        if self.active:
            duration = duration or timedelta(
                minutes=self.DEFAULT_DURATION_MINUTES)
            self.end = datetime.now() + duration
            self.token = str(uuid4())
            self.login = False
            return self.save()
        else:
            return False

    def todict(self):
        """Converts the session to a dictionary"""
        result = {}
        result['account'] = self.account.name
        result['token'] = self.token
        result['start'] = str(self.start)
        result['end'] = str(self.end)
        result['login'] = True if self.login else False
        return result


tables = [Service, CustomerService, Account, AccountService, Session]
