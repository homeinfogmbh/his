"""Group and user definitions"""

from datetime import datetime, timedelta
from uuid import uuid4
from importlib import import_module

from peewee import Model, PrimaryKeyField, ForeignKeyField,\
    CharField, BooleanField, DateTimeField, IntegerField, DoesNotExist

from homeinfo.lib.misc import classproperty
from homeinfo.lib.strf import cc2jl
from homeinfo.peewee import MySQLDatabase
from homeinfo.crm import Customer, Employee

from his.api.errors import InvalidCredentials, AccountLocked
from his.config import config
from his.crypto import verify_password

__all__ = [
    'service_table',
    'HISModel',
    'Service',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'tables']

database = MySQLDatabase(
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


def service_table(module, name=None):
    """Makes a model definition a HIS service database table"""

    def wrap(model):
        if name is None:
            model._meta.db_table = '_'.join((module, cc2jl(model.__name__)))
        else:
            model._meta.db_table = '_'.join((module, name))

        return model

    return wrap


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
                    'Cannot enable service {service} for account {account}, '
                    'because the respective customer {customer} is not '
                    'enabled for it'.format(
                        service=service, account=self.account,
                        customer=self.account.customer))

    def remove(self, service):
        """Removes a service from the mapping"""
        for account_service in AccountService.select().where(
                (AccountService.account == self.account) &
                (AccountService.service == service)):
            account_service.delete_instance()


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model"""

    class Meta:
        database = database
        schema = database.database

    id = PrimaryKeyField()


class Service(HISModel):
    """Registers services of HIS"""

    node = CharField(255)
    module = CharField(255)
    class_ = CharField(32, db_column='class', null=True, default=None)
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

    @property
    def handler(self):
        """Loads the appropriate handler"""
        module = import_module(self.module)
        class_ = self.class_ or 'App'
        return getattr(module, class_)


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping"""

    class Meta:
        db_table = 'customer_service'

    customer = ForeignKeyField(Customer, db_column='account')
    service = ForeignKeyField(Service, db_column='service')
    begin = DateTimeField(null=True, default=None)
    end = DateTimeField(null=True, default=None)

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

    def remove(self):
        """Safely removes a customer service and its dependencies"""
        for account_service in AccountService.select().where(
                (AccountService.account.customer == self.customer) &
                (AccountService.service == self.service)):
            account_service.delete_instance()

        self.delete_instance()


class Account(HISModel):
    """A HIS login account"""

    customer = ForeignKeyField(
        Customer, db_column='customer',
        related_name='accounts')
    user = ForeignKeyField(
        Employee, db_column='user', null=True,
        related_name='accounts')
    name = CharField(64)
    pwhash = CharField(255)
    email = CharField(64)
    created = DateTimeField()
    deleted = DateTimeField(null=True, default=None)
    last_login = DateTimeField(null=True, default=None)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True, default=None)
    disabled = BooleanField(default=True)
    # Flag, whether the account is an
    # administrator of its company
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

    @classmethod
    def find(cls, id_or_name):
        """Find account by primary key or login name"""
        try:
            ident = int(id_or_name)
        except ValueError:
            return cls.get(cls.name == id_or_name)
        else:
            return cls.get(cls.id == ident)

    @property
    def valid(self):
        """Determines whether the account is valid"""
        return self.pwhash and not self.deleted and not self.disabled

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if self.locked_until is None:
            return False
        else:
            return self.locked_until >= datetime.now()

    @property
    def active(self):
        """Determines whether the account has an open session"""
        for session in Session.select().where(Session.account == self):
            if session.alive:
                return True

        return False

    @property
    def services(self):
        """Yields appropriate services"""
        return AccountServicesWrapper(self)

    @property
    def subjects(self):
        """Yields accounts this account can manage"""
        # All accounts can manage theirselves
        yield self

        # Admins can manage accounts of their
        # company, i.e. the same customer
        if self.admin:
            yield from Account.select().where(
                Account.customer == self.customer)

            # If the company is a reseller, they can
            # manage all accounts of the resold companies
            for customer in self.customer.resales:
                yield from Account.select().where(Account.customer == customer)

    def login(self, passwd):
        """Performs a login"""
        if self.valid and verify_password(self.pwhash, passwd):
            if not self.locked:
                self.last_login = datetime.now()
                self.save()
                return Session.open(self)
            else:
                raise AccountLocked(self.locked_until) from None
        else:
            raise InvalidCredentials() from None


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping"""

    class Meta:
        db_table = 'account_service'

    account = ForeignKeyField(Account, db_column='account')
    service = ForeignKeyField(Service, db_column='service')


class Session(HISModel):
    """A session related to an account"""

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
        return '{start} - {end}: {token} ({login})'.format(
            start=self.start, end=self.end, token=self.token, login=self.login)

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
    def open(cls, account, duration=None):
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

    @property
    def alive(self):
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
        if self.alive:
            duration = duration or timedelta(
                minutes=self.DEFAULT_DURATION_MINUTES)
            self.end = datetime.now() + duration
            self.token = str(uuid4())
            self.login = False
            return self.save()
        else:
            return False

    def to_dict(self):
        """Converts the session to a dictionary"""
        return {
            'account': self.account.name,
            'token': self.token,
            'start': str(self.start),
            'end': str(self.end),
            'login': True if self.login else False}


tables = [Service, CustomerService, Account, AccountService, Session]
