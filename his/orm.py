"""Group and user definitions."""

from datetime import datetime, timedelta
from uuid import uuid4
from contextlib import suppress
from importlib import import_module

from peewee import Model, PrimaryKeyField, ForeignKeyField,\
    CharField, BooleanField, DateTimeField, IntegerField, DoesNotExist

from peeweeplus import MySQLDatabase
from timelib import strpdatetime
from filedb import FileProperty

from homeinfo.misc import classproperty
from homeinfo.crm import Customer, Employee

from his.api.messages import InvalidCredentials, AccountLocked, \
    DurationOutOfBounds
from his.config import CONFIG
from his.crypto import hash_password, verify_password

__all__ = [
    'AccountExists',
    'AmbiguousDataError',
    'his_db',
    'HISModel',
    'Service',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'CustomerSettings',
    'MODELS']

DATABASE = MySQLDatabase(
    CONFIG['db']['db'],
    host=CONFIG['db']['HOST'],
    user=CONFIG['db']['USER'],
    passwd=CONFIG['db']['PASSWD'],
    closing=True)


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class AccountExists(Exception):
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


def his_db(service_name):
    """Returns a database for the respective service."""

    return MySQLDatabase(
        'his_{}'.format(service_name),
        host=CONFIG['db']['HOST'],
        user=CONFIG['db']['USER'],
        passwd=CONFIG['db']['PASSWD'],
        closing=True)


class AccountServicesProxy():
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

    def remove(self, service):
        """Removes a service from the account's mapping."""
        for account_service in AccountService.select().where(
                (AccountService.account == self.account) &
                (AccountService.service == service)):
            account_service.delete_instance()


class HISModel(Model):
    """Generic HOMEINFO Integrated Service database model."""

    class Meta:
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()


class Service(HISModel):
    """Registers services of HIS."""

    name = CharField(32, null=True, default=None)
    description = CharField(255, null=True, default=None)
    # Flag whether the service shall be promoted
    promote = BooleanField(default=True)

    def __str__(self):
        """Returns the service's name."""
        return self.name


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping."""

    class Meta:
        db_table = 'customer_service'

    customer = ForeignKeyField(Customer, db_column='account')
    service = ForeignKeyField(Service, db_column='service')
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
        Customer, db_column='customer', related_name='accounts')
    user = ForeignKeyField(
        Employee, db_column='user', null=True, related_name='accounts')
    name = CharField(64)
    pwhash = CharField(255)
    email = CharField(64)
    created = DateTimeField()
    deleted = DateTimeField(null=True, default=None)
    last_login = DateTimeField(null=True, default=None)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True, default=None)
    disabled = BooleanField(default=False)
    # Flag, whether the account is an
    # administrator of its customer (=company)
    admin = BooleanField(default=False)
    # Flag, whether the user is a super-admin of the system
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
    def add(cls, customer, name, email, passwd=None, pwhash=None, user=None):
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

                if passwd is not None and pwhash is not None:
                    raise ValueError('Must specify either passwd or pwhash.')
                elif passwd is not None:
                    account.passwd = passwd
                elif pwhash is not None:
                    account.pwhash = pwhash
                else:
                    raise ValueError('Must specify either passwd or pwhash.')

                account.user = user
                return account

            raise AccountExists('name') from None

        raise AccountExists('email') from None

    @classmethod
    def admins(cls, customer=None):
        """Yields administrators."""
        if customer is None:
            return cls.select().where(cls.admin == 1)

        return cls.select().where(
            (cls.customer == customer) & (cls.admin == 1))

    @classmethod
    def find(cls, id_or_name):
        """Find account by primary key or login name."""
        try:
            ident = int(id_or_name)
        except ValueError:
            return cls.get(cls.name == id_or_name)

        return cls.get(cls.id == ident)

    def passwd(self, passwd):
        """Sets the password."""
        self.pwhash = hash_password(passwd)

    passwd = property(None, passwd)

    @property
    def valid(self):
        """Determines whether the account is valid."""
        return self.pwhash and not self.deleted and not self.disabled

    @property
    def locked(self):
        """Determines whether the user is locked."""
        if self.failed_logins > 5:
            return True
        elif self.locked_until is not None:
            return self.locked_until >= datetime.now()

        return False

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
        # All accounts can manage themselves.
        yield self

        # Admins can manage accounts of their
        # company, i.e. the same customer.
        if self.admin:
            for account in self.__class__.select().where(
                    self.__class__.customer == self.customer):
                # We already yielded this very account.
                if account != self:
                    yield account

    def login(self, passwd):
        """Performs a login."""
        if self.valid and not self.locked:
            if verify_password(self.pwhash, passwd):
                self.failed_logins = 0
                self.last_login = datetime.now()
                self.save()
                return True

            self.failed_logins += 1
            self.save()
            raise InvalidCredentials() from None

        raise AccountLocked() from None

    def to_dict(self):
        """Returns the account as a JSON-like dictionary."""
        dictionary = {
            'customer': self.customer.id,
            'name': self.name,
            'email': self.email,
            'created': self.created.isoformat(),
            'failed_logins': self.failed_logins,
            'disabled': self.disabled,
            'admin': self.admin,
            'root': self.root}

        if self.user is not None:
            dictionary['user'] = self.user.id

        if self.deleted is not None:
            dictionary['deleted'] = self.deleted.isoformat()

        if self.last_login is not None:
            dictionary['last_login'] = self.last_login.isoformat()

        if self.locked_until is not None:
            dictionary['locked_until'] = self.locked_until.isoformat()

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
                raise AmbiguousDataError('email') from None

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
                raise AmbiguousDataError('name') from None

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
        db_table = 'account_service'

    account = ForeignKeyField(Account, db_column='account')
    service = ForeignKeyField(Service, db_column='service')

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

    account = ForeignKeyField(Account, db_column='account')
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

    def to_dict(self):
        """Converts the session to a dictionary."""
        return {
            'account': self.account.name,
            'token': self.token,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'login': self.login}


class CustomerSettings(HISModel):
    """Settings for a certain customer."""

    class Meta:
        db_table = 'customer_settings'

    customer = ForeignKeyField(Customer, db_column='customer')
    max_accounts = IntegerField(null=True, default=10)
    _logo = IntegerField(db_column='logo', null=True)
    logo = FileProperty(_logo)


MODELS = [Service, CustomerService, Account, AccountService, Session]
