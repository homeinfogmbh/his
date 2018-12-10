"""ORM models."""

from datetime import datetime, timedelta
from email.utils import parseaddr
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import UUIDField

from filedb import FileProperty
from mdb import Customer
from peeweeplus import InvalidKeys, MySQLDatabase, JSONModel, Argon2Field

from his.config import CONFIG
from his.exceptions import AccountExistsError
from his.exceptions import InconsistencyError
from his.exceptions import PasswordResetPending
from his.exceptions import ServiceExistsError
from his.messages import AccountLocked, InvalidCredentials, DurationOutOfBounds
from his.pwmail import mail_password_reset_link


__all__ = [
    'HISModel',
    'Service',
    'ServiceDependency',
    'ServiceDomain',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'CustomerSettings',
    'PasswordResetToken',
    'MODELS']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


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

            for dependency in account_service.service.dependencies:
                yield dependency.dependency

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

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Service(HISModel):
    """Registers services of HIS."""

    name = CharField(32, null=True)
    description = CharField(255, null=True)
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

        if self in CustomerService.services(account.customer):
            return account.admin or self in account.services

        return False


class ServiceDependency(HISModel):
    """Maps service dependencies."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_dependency'

    service = ForeignKeyField(
        Service, column_name='service', backref='dependencies',
        on_delete='CASCADE')
    dependency = ForeignKeyField(
        Service, column_name='dependency', on_delete='CASCADE')


class ServiceDomain(HISModel):
    """Domains for the respective services."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_domain'

    service = ForeignKeyField(
        Service, column_name='service', backref='domains', on_delete='CASCADE')
    domain = CharField(255)


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_service'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', on_delete='CASCADE')
    begin = DateTimeField(null=True)
    end = DateTimeField(null=True)

    def __str__(self):
        return '{}@{}'.format(repr(self.customer), str(self.service))

    @classmethod
    def add(cls, customer, service, begin=None, end=None):
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

            for dependency in customer_service.service.dependencies:
                yield dependency.dependency

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
    name = CharField(64, unique=True)   # Login name.
    full_name = CharField(255, null=True)   # Optional full user name.
    passwd = Argon2Field()
    email = CharField(64, unique=True)
    created = DateTimeField(default=datetime.now)
    deleted = DateTimeField(null=True)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True)
    disabled = BooleanField(default=False)
    # Flag, whether the account is an administrator of its customer (=company).
    admin = BooleanField(default=False)
    # Flag, whether the account is root.
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

    @classmethod
    def add(cls, customer, name, email, passwd, admin=False, root=False):
        """Adds a new account."""
        if len(name) < 3:
            raise ValueError('Account name too short.')

        _, email = parseaddr(email)

        if len(email) < 6 or '@' not in email:
            raise ValueError('Invalid email address.')

        try:
            cls.get(cls.email == email)
        except cls.DoesNotExist:
            pass
        else:
            raise AccountExistsError('email')

        try:
            cls.get(cls.name == name)
        except cls.DoesNotExist:
            pass
        else:
            raise AccountExistsError('name')

        account = cls()
        account.customer = customer
        account.name = name
        account.email = email
        account.created = datetime.now()
        account.passwd = passwd
        account.admin = admin
        account.root = root
        return account


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

    @property
    def locked(self):
        """Determines whether the account is locked."""
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
        cls = type(self)

        if self.root:
            yield from cls
        elif self.admin:
            for account in cls.select().where(cls.customer == self.customer):
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
            try:
                self.passwd.verify(passwd)
            except VerifyMismatchError:
                self.failed_logins += 1
                self.save()
                raise InvalidCredentials()

            if self.passwd.needs_rehash:
                self.passwd = passwd

            self.failed_logins = 0
            self.last_login = datetime.now()
            self.save()
            return True

        raise AccountLocked()

    def patch_json(self, json, allow=(), **kwargs):
        """Patches the account with fields limited to allow."""
        invalid = {key for key in json if key not in allow} if allow else None

        if invalid:
            raise InvalidKeys(invalid)

        return super().patch_json(json, **kwargs)


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping."""

    class Meta:     # pylint: disable=C0111,R0903
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
    token = UUIDField(default=uuid4)
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField(default=True)

    def __repr__(self):
        """Returns a unique string representation."""
        return self.token.hex

    def __str__(self):
        """Returns a human-readable representation."""
        return '{} - {}: {} ({})'.format(
            self.start.isoformat(), self.end.isoformat(), self.token.hex,
            self.login)

    @classmethod
    def add(cls, account, duration):
        """Actually opens a new login session."""
        now = datetime.now()
        session = cls()
        session.account = account
        session.start = now
        session.end = now + duration
        return session

    @classmethod
    def open(cls, account, duration=15):
        """Actually opens a new login session."""
        if duration not in cls.ALLOWED_DURATIONS:
            raise DurationOutOfBounds()

        duration = timedelta(minutes=duration)
        session = cls.add(account, duration)
        session.save()
        return session

    @classmethod
    def cleanup(cls, before=None):
        """Cleans up orphaned sessions."""
        if before is None:
            before = datetime.now()

        for session in cls.select().where(cls.end < before):
            session.delete_instance()
            yield session

    @property
    def alive(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() < self.end

    def renew(self, duration=15):
        """Renews the session."""
        if duration not in type(self).ALLOWED_DURATIONS:
            raise DurationOutOfBounds()

        if not self.account.can_login:
            raise AccountLocked()

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self


class CustomerSettings(HISModel):
    """Settings for a certain customer."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_settings'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    max_accounts = IntegerField(null=True, default=10)
    _logo = IntegerField(column_name='logo', null=True)
    logo = FileProperty(_logo)


class PasswordResetToken(HISModel):
    """Tokens to reset passwords."""

    VALIDITY = timedelta(hours=1)

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'password_reset_token'

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    token = UUIDField(default=uuid4)
    created = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, account):
        """Adds a new password reset token."""
        try:
            record = cls.get(cls.account == account)
        except cls.DoesNotExist:
            record = cls()
            record.account = account
            return record

        if record.valid:
            raise PasswordResetPending()

        record.delete_instance()
        return cls.add(account)

    @property
    def valid(self):
        """Determines whether the token is still valid."""
        return self.created + self.VALIDITY > datetime.now()

    def email(self, url):
        """Emails the reset link to the respective account."""
        return mail_password_reset_link(self, url)


MODELS = (
    Service, ServiceDomain, CustomerService, Account, AccountService, Session,
    CustomerSettings, PasswordResetToken)
