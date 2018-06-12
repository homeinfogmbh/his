"""ORM models."""

from datetime import datetime, timedelta
from uuid import uuid4
from contextlib import suppress

from peewee import PrimaryKeyField, ForeignKeyField, CharField, BooleanField, \
    DateTimeField, IntegerField, DoesNotExist

from filedb import FileProperty
from homeinfo.crm import Customer, Employee
from homeinfo.misc import classproperty
from peeweeplus import MySQLDatabase, JSONModel
from timelib import strpdatetime

from his.config import CONFIG
from his.crypto import hash_password, verify_password
from his.messages import AccountLocked, InvalidCredentials, DurationOutOfBounds

__all__ = [
    'ServiceExistsError',
    'AccountExistsError',
    'AmbiguousDataError',
    'HISModel',
    'Service',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'CustomerSettings',
    'MODELS']

DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""

    pass


class AccountExistsError(Exception):
    """Indicates that the respective account already exists."""

    def __init__(self, field):
        super().__init__(field)
        self.field = field


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""

    def __init__(self, field):
        super().__init__(field)
        self.field = field

    def __str__(self):
        return self.field


class AccountServicesProxy:
    """Proxy to transparently handle an account's services."""

    def __init__(self, account):
        """Sets the respective account."""
        self.account = account

    def __iter__(self):
        """Yields appropriate services."""
        for account_service in AccountService.select().where(
                AccountService.account == self.account):
            yield account_service.service

    def add(self, service):
        """Maps a service to this account."""
        if service not in self:
            if service in CustomerService.services(self.account.customer):
                account_service = AccountService()
                account_service.account = self.account
                account_service.service = service
                account_service.save()
                return True

            raise InconsistencyError(
                'Cannot enable service {} for account {}, because the '
                'respective customer {} is not enabled for it.'.format(
                    service, self.account, self.account.customer))

        return False

    def remove(self, service):
        """Removes a service from the account's mapping."""
        for account_service in AccountService.select().where(
                (AccountService.account == self.account) &
                (AccountService.service == service)):
            account_service.delete_instance()


class HISModel(JSONModel):
    """Generic HOMEINFO Integrated Service database model."""

    class Meta:
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()


class Service(HISModel):
    """Registers services of HIS."""

    name = CharField(32, null=True, default=None)
    description = CharField(255, null=True, default=None)
    # Flag whether the service shall be promoted.
    promote = BooleanField(default=True)

    def __str__(self):
        """Returns the service's name."""
        return self.name

    @classmethod
    def add(cls, name, description=None, promote=True):
        """Adds a new service."""
        try:
            cls.get(cls.name == name)
        except cls.DoesNotExist:
            service = cls()
            service.name = name
            service.description = description
            service.promote = promote
            return service

        raise ServiceExistsError()

    def authorized(self, account):
        """Determines whether the respective account
        is authorized to use this service.

        An account is considered authorized if:
            1) account is root or
            2) account's customer is enabled for the service and
                2a) account is admin or
                2b) account is enabled for the service
        """
        if account.root:
            return True
        elif self in CustomerService.services(account.customer):
            return account.admin or self in account.services

        return False


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping."""

    class Meta:
        table_name = 'customer_service'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', on_delete='CASCADE')
    begin = DateTimeField(null=True, default=None)
    end = DateTimeField(null=True, default=None)

    def __str__(self):
        return '{}@{}'.format(repr(self.customer), str(self.service))

    @classmethod
    def add(cls, customer, service, begin, end):
        """Adds a new customer service."""
        customer_service = cls()
        customer_service.customer = customer
        customer_service.service = service
        customer_service.begin = begin
        customer_service.end = end
        return customer_service

    @classmethod
    def services(cls, customer):
        """Yields services for the respective customer."""
        for customer_service in cls.select().where(cls.customer == customer):
            yield customer_service.service

    @property
    def active(self):
        """Determines whether the service mapping is active."""
        if self.begin is None:
            if self.end is None:
                return True

            return datetime.now() < self.end

        if self.end is None:
            return datetime.now() >= self.begin

        return self.begin <= datetime.now() < self.end

    def remove(self):
        """Safely removes a customer service and its dependencies."""
        for account_service in AccountService.select().where(
                (AccountService.account.customer == self.customer) &
                (AccountService.service == self.service)):
            account_service.delete_instance()

        self.delete_instance()


class Account(HISModel):
    """A HIS account."""

    customer = ForeignKeyField(
        Customer, column_name='customer', related_name='accounts')
    user = ForeignKeyField(
        Employee, column_name='user', null=True, related_name='accounts')
    name = CharField(64)
    _pwhash = CharField(255, column_name='pwhash')
    email = CharField(64)
    created = DateTimeField(default=datetime.now)
    deleted = DateTimeField(null=True, default=None)
    last_login = DateTimeField(null=True, default=None)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True, default=None)
    disabled = BooleanField(default=False)
    # Flag, whether the account is an administrator of its customer (=company).
    admin = BooleanField(default=False)
    # Flag, whether the user is a super-admin of the system.
    # Such accounts can do ANYTHING!
    root = BooleanField(default=False)

    def __int__(self):
        """Returns the account's ID."""
        return self.id

    def __repr__(self):
        """Returns the account's login name."""
        return self.name

    def __str__(self):
        """Returns the login name and appropriate customer."""
        return '{}@{}'.format(repr(self), self.customer.id)

    @classproperty
    @classmethod
    def superadmins(cls):
        """Yields all root users aka. super-admins."""
        return cls.select().where(cls.root == 1)

    @classmethod
    def add(cls, customer, name, email, passwd, user=None, admin=False,
            root=False):
        """Adds a new account."""
        try:
            cls.get(cls.email == email)
        except DoesNotExist:
            try:
                cls.get(cls.name == name)
            except DoesNotExist:
                account = cls()
                account.customer = customer
                account.name = name
                account.email = email
                account.created = datetime.now()
                account.passwd = passwd
                account.user = user
                account.admin = admin
                account.root = root
                return account

            raise AccountExistsError('name')

        raise AccountExistsError('email')

    @classmethod
    def admins(cls, customer=None):
        """Yields administrators."""
        if customer is None:
            return cls.select().where(cls.admin == 1)

        return cls.select().where(
            (cls.customer == customer) & (cls.admin == 1))

    @classmethod
    def find(cls, id_or_name, customer=None):
        """Find account by primary key or login name."""
        customer_expr = True if customer is None else cls.customer == customer

        try:
            ident = int(id_or_name)
        except ValueError:
            sel_expr = cls.name == id_or_name
        else:
            sel_expr = cls.id == ident

        return cls.get(customer_expr & sel_expr)

    def passwd(self, passwd):
        """Sets the password."""
        self._pwhash = hash_password(passwd)

    passwd = property(None, passwd)

    @property
    def locked(self):
        """Determines whether the user is locked."""
        if self.locked_until is None:
            return False

        return self.locked_until >= datetime.now()

    @property
    def usable(self):
        """Determines whether the account is currently usable."""
        return not self.deleted and not self.disabled and not self.locked

    @property
    def failed_logins_exceeded(self):
        """Determines whether the account has exceeded
        the acceptable amount of failed logins.
        """
        return self.failed_logins > 5

    @property
    def can_login(self):
        """Determines whether the account can log in."""
        return self.usable and not self.failed_logins_exceeded

    @property
    def active(self):
        """Determines whether the account has an open session."""
        for session in Session.select().where(Session.account == self):
            if session.alive:
                return True

        return False

    @property
    def services(self):
        """Returns an account <> service mapping proxy."""
        return AccountServicesProxy(self)

    @property
    def subjects(self):
        """Yields accounts this account can manage."""
        if self.root:
            yield from self.__class__
        elif self.admin:
            for account in self.__class__.select().where(
                    self.__class__.customer == self.customer):
                yield account
        else:
            yield self

    @property
    def info(self):
        """Returns brief account information."""
        return {'id': self.id, 'email': self.email}

    def login(self, passwd):
        """Performs a login."""
        if self.can_login:
            if verify_password(self._pwhash, passwd):
                self.failed_logins = 0
                self.last_login = datetime.now()
                self.save()
                return True

            self.failed_logins += 1
            self.save()
            raise InvalidCredentials()

        raise AccountLocked()

    def to_dict(self, null=False, **kwargs):
        """Returns the account as a JSON-like dictionary."""
        dictionary = super().to_dict(null=null, **kwargs)
        dictionary['customer'] = self.customer.id

        if self.user is not None:
            dictionary['user'] = self.user.to_dict()
        elif null:
            dictionary['user'] = None

        return dictionary

    def patch(self, dictionary):
        """Patches the record from a JSON-like dictionary."""
        try:
            email = dictionary['email']
        except KeyError:
            pass
        else:
            try:
                self.__class__.get(self.__class__.email == email)
            except DoesNotExist:
                self.email = email
            else:
                raise AmbiguousDataError('email')

        with suppress(KeyError):
            self.passwd = dictionary['passwd']

        with suppress(KeyError):
            self.admin = dictionary['admin']

        with suppress(KeyError):
            self.customer = Customer.get(
                Customer.id == dictionary['customer'])

        with suppress(KeyError):
            self.user = Employee.get(Employee.id == dictionary['user'])

        try:
            name = dictionary['name']
        except KeyError:
            pass
        else:
            try:
                self.__class__.get(self.__class__.name == name)
            except DoesNotExist:
                self.name = name
            else:
                raise AmbiguousDataError('name')

        with suppress(KeyError):
            self.failed_logins = dictionary['failed_logins']

        with suppress(KeyError):
            self.locked_until = strpdatetime(dictionary['locked_until'])

        with suppress(KeyError):
            self.disabled = dictionary['disabled']

        return self


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping."""

    class Meta:
        table_name = 'account_service'

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', on_delete='CASCADE')

    def __str__(self):
        return '{}@{}'.format(str(self.account), str(self.service))

    @classmethod
    def add(cls, account, service):
        """Adds a new account service."""
        account_service = cls()
        account_service.account = account
        account_service.service = service
        return account_service


class Session(HISModel):
    """A session related to an account."""

    ALLOWED_DURATIONS = range(5, 31)

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    token = CharField(64)   # A uuid4
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField()  # Login session or keep-alive?

    def __repr__(self):
        """Returns a unique string representation."""
        return self.token

    def __str__(self):
        """Returns a human-readable representation."""
        return '{} - {}: {} ({})'.format(
            self.start.isoformat(), self.end.isoformat(), self.token,
            self.login)

    @classmethod
    def open(cls, account, duration=15):
        """Actually opens a new login session."""
        now = datetime.now()

        if duration in cls.ALLOWED_DURATIONS:
            duration = timedelta(minutes=duration)
            session = cls()
            session.account = account
            session.token = str(uuid4())
            session.start = now
            session.end = now + duration
            session.login = True
            session.save()
            return session

        raise DurationOutOfBounds()

    @classmethod
    def cleanup(cls, before=None):
        """Cleans up orphaned sessions."""
        cleaned_up = []

        if before is None:
            before = datetime.now()

        for session in cls.select().where(cls.end < before):
            cleaned_up.append(session)
            session.close()

        return cleaned_up

    @property
    def alive(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() < self.end

    def reload(self):
        """Re-loads the session information from the database."""
        return self.__class__.get(
            (self.__class__.account == self.account) &
            (self.__class__.token == self.token) &
            (self.__class__.start == self.start) &
            (self.__class__.end == self.end) &
            (self.__class__.login == self.login))

    def close(self):
        """Closes the session."""
        return self.delete_instance()

    def renew(self, duration=15):
        """Renews the session."""
        if duration in self.ALLOWED_DURATIONS:
            if self.alive:
                self.end = datetime.now() + timedelta(minutes=duration)
                self.login = False
                self.save()
                return True

            return False

        raise DurationOutOfBounds()

    def to_dict(self, **kwargs):
        """Converts the session to a dictionary."""
        dictionary = super().to_dict(**kwargs)
        dictionary['account'] = self.account.name
        return dictionary


class CustomerSettings(HISModel):
    """Settings for a certain customer."""

    class Meta:
        table_name = 'customer_settings'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    max_accounts = IntegerField(null=True, default=10)
    _logo = IntegerField(column_name='logo', null=True)
    logo = FileProperty(_logo)


MODELS = (Service, CustomerService, Account, AccountService, Session)
