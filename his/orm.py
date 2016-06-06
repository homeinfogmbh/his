"""Group and user definitions"""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import Model, PrimaryKeyField, ForeignKeyField,\
    CharField, BooleanField, DateTimeField, IntegerField, DoesNotExist

from homeinfo.lib.misc import classproperty
from homeinfo.peewee import MySQLDatabase, create
from homeinfo.crm import Customer, Employee

from ..config import his_config

__all__ = [
    'his_db',
    'HISServiceDatabase',
    'HISModel',
    'Service',
    'CustomerServices',
    'Account',
    'AccountServices',
    'User',
    'Login']


his_db = MySQLDatabase(
    his_config.db['db'],
    host=his_config.db['HOST'],
    user=his_config.db['USER'],
    passwd=his_config.db['PASSWD'],
    closing=True)


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration"""

    pass


class AlreadyLoggedIn(Exception):
    """Indicates that a session is already open for the respective account"""

    pass


class HISServiceDatabase(MySQLDatabase):
    """A HIS service database
    Gets the name of the service, prefixed by the master database
    """

    def __init__(self, service, host=None, user=None, passwd=None, **kwargs):
        """Initializes the database with the respective service's
        name and optional diverging database configuration
        """
        if host is None:
            host = his_config.db['host']

        if user is None:
            user = his_config.db['user']

        if passwd is None:
            passwd = his_config.db['passwd']

        # Change the name to create a '_'-separated namespace
        super().__init__(
            '_'.join((his_config.db['db'], repr(service))),
            host=host, user=user, passwd=passwd, closing=True, **kwargs)


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model"""

    class Meta:
        database = his_db
        schema = database.database

    id = PrimaryKeyField()


class Service(HISModel):
    """Registers services of HIS"""

    name = CharField(32)
    description = CharField(255, null=True, default=None)
    # Flag whether the service shall be promoted
    promote = BooleanField(default=True)

    def __repr__(self):
        """Returns the service's ID as a string"""
        return str(self.id)

    def __str__(self):
        """Returns the service's name"""
        if self.description is not None:
            return '{0} ({1})'.format(self.name, self.description)
        else:
            return self.name


@create
class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping"""

    class Meta:
        db_table = customer_service

    customer = ForeignKeyField(
        Customer, db_column='account',
        related_name='customer_services')
    service = ForeignKeyField(
        Service, db_column='service',
        related_name='service_customers')

    def remove(self):
        """Safely removes a customer service and its dependencies"""
        for account_service in AccountService.select().where(
                (AccountService.account.customer == self.customer) &
                (AccountService.service == self.service)):
            account_service.delete_instance()


@create
class Account(HISModel):
    """A HIS login account"""

    class ServicesWrapper():
        """Wraps service mappings with manipulation options"""

        def __init__(self, account):
            self.account = account

        def __iter__(self):
            for account_service in AccountService.select().where(
                    AccountServices.account == self.account):
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
            if service in self:
                account_service = AccountService.get(
                    (AccountService.account == self.account) &
                    (AccountService.service == service))
                account_service.delete_instance()

    customer = ForeignKeyField(
        Customer, db_column='customer',
        related_name='accounts')
    user = ForeignKeyField(
        Employee, db_column='user', null=True,
        related_name='accounts')
    name = CharField(64)  # Login name
    pwhash = CharField(64)  # SHA-256 hash
    salt = CharField(32)  # Password salt (HMAC)
    email = CharField(64)
    created = DateTimeField()
    deleted = DateTimeField(null=True)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField()
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
        elif self.locked_until - datetime.now() > timedelta(0):
            return True
        else:
            return False

    @property
    def services(self):
        """Yields appropriate services"""
        return ServicesWrapper(self)


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping"""

    class Meta:
        db_table = account_service

    account = ForeignKeyField(Account, db_column='account')
    service = ForeignKeyField(Service, db_column='service')


@create
class Session(HISModel):
    """A session related to a login"""

    account = ForeignKeyField(Account, db_column='account')
    token = CharField(64)   # A uuid4
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField()  # Login session or keep-alive?

    def __bool__(self):
        """Returns a boolean representation"""
        try:
            myself = self.refresh()
        except DoesNotExist:
            return False
        else:
            return (datetime.now() - myself.end) > timedelta(0)

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
        duration = duration or timedelta(minutes=5)
        session = cls()
        session.account = account
        session.token = str(uuid4())
        session.start = now
        session.end = now + duration
        session.login = True
        session.save()
        return True

    @classmethod
    def open(cls, account, duration=None):
        """Opens a login session for the specified account
        XXX: This must only be done after successful login
        """
        try:
            active_session = cls.get(cls.account == account)
        except DoesNotExist:
            return cls._open(account, duration=duration)
        else:
            if active_session:
                raise AlreadyLoggedIn()
            else:
                active_session.close()
                return cls._open(account, duration=duration)

    def refresh(self):
        """Refreshes the session information from the database"""
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
        if self:
            now = datetime.now()
            duration = duration or timedelta(minutes=5)
            self.end = now + duration
            self.token = str(uuid4())
            self.login = False
            return self.save()
        else:
            return False
