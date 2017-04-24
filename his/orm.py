"""Group and user definitions"""

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
from his.api.share import file_client
from his.config import config
from his.crypto import passwd_hasher, verify_password

__all__ = [
    'AccountExists',
    'AmbiguousDataError',
    'module_db',
    'module_model',
    'HISModel',
    'Service',
    'CustomerService',
    'Account',
    'AccountService',
    'Session',
    'CustomerSettings',
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


class AccountExists(Exception):
    """Indicates that the respective account already exists"""

    def __init__(self, field):
        super().__init__(field)
        self.field = field


class AmbiguousDataError(Exception):
    """Indicates that two passwords do not match"""

    def __init__(self, field):
        self.field = field

    def __str__(self):
        return self.field


def check_service_consistency(customer=None):
    """Check service assignment consistency"""

    pass  # TODO: Implement


def module_db(module):
    """Returns a database for the respective sub-module"""

    return MySQLDatabase(
        '_'.join((config.db['db'], module)),
        host=config.db['HOST'],
        user=config.db['USER'],
        passwd=config.db['PASSWD'],
        closing=True)


def module_model(module):
    """Returns a base module for the respective module"""

    class ModuleModel(HISModel, LoggingClass):
        """Module model wrapper class"""

        class Meta:
            database = module_db(module)
            schema = database.database

        def __init__(self, *args, logger=None, **kwargs):
            """initializes the super classes"""
            HISModel.__init__(self, *args, **kwargs)
            LoggingClass.__init__(self, logger=logger)

    return ModuleModel


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
    disabled = BooleanField(default=False)
    # Flag, whether the account is an
    # administrator of its customer (=company)
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
    def add(cls, customer, name, email, passwd=None, pwhash=None, user=None,
            locked_until=None, disabled=None, admin=None, root=None):
        """Adds a new account"""
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

                if passwd is not None and pwhash is not None:
                    raise ValueError('Must specify either passwd or pwhash')
                elif passwd is not None:
                    account.passwd = passwd
                elif pwhash is not None:
                    account.pwhash = pwhash
                else:
                    raise ValueError('Must specify either passwd or pwhash')

                account.user = user
                account.locked_until = locked_until

                if disabled is not None:
                    account.disabled = disabled

                if admin is not None:
                    account.admin = admin

                if root is not None:
                    account.root = root

                return account
            else:
                raise AccountExists('name')
        else:
            raise AccountExists('email')

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

    @classmethod
    def of(cls, customer):
        """Yields the accounts of the respective customer"""
        return cls.select().where(cls.customer == customer)

    def passwd(self, passwd):
        """Sets the password"""
        self.pwhash = passwd_hasher.hash(passwd)

    passwd = property(None, passwd)

    @property
    def valid(self):
        """Determines whether the account is valid"""
        return self.pwhash and not self.deleted and not self.disabled

    @property
    def locked(self):
        """Determines whether the user is locked"""
        if self.failed_logins > 5:
            return True
        elif self.locked_until is not None:
            return self.locked_until >= datetime.now()
        else:
            return False

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
        if self.valid and not self.locked:
            if verify_password(self.pwhash, passwd):
                self.failed_logins = 0
                self.last_login = datetime.now()
                self.save()
                return True
            else:
                self.failed_logins += 1
                self.save()
                raise InvalidCredentials() from None
        else:
            raise AccountLocked() from None

    def to_dict(self):
        """Returns the account as a JSON-like dictionary"""
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

    def patch(self, d):
        """Patches the record from a JSON-like dictionary"""
        try:
            email = d['email']
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
            self.passwd = d['passwd']

        with suppress(KeyError):
            self.admin = d['admin']

        with suppress(KeyError):
            self.customer = Customer.get(Customer.id == int(d['customer']))

        with suppress(KeyError):
            self.user = Employee.get(Employee.id == int(d['user']))

        try:
            name = d['name']
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
            self.failed_logins = d['failed_logins']

        with suppress(KeyError):
            self.locked_until = strpdatetime(locked_until=d['locked_until'])

        with suppress(KeyError):
            self.disabled = d['disabled']

        return self


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping"""

    class Meta:
        db_table = 'account_service'

    account = ForeignKeyField(Account, db_column='account')
    service = ForeignKeyField(Service, db_column='service')


class Session(HISModel):
    """A session related to an account"""

    ALLOWED_DURATIONS = range(5, 21)

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
            start=self.start.isoformat(), end=self.end.isoformat(),
            token=self.token, login=self.login)

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
    def open(cls, account, duration=15):
        """Actually opens a new login session"""
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
        else:
            raise DurationOutOfBounds()

    @classmethod
    def cleanup(cls):
        """Cleans up orphaned sessions"""
        now = datetime.now()

        for session in cls:
            if session.end < now:
                session.close()

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

    def renew(self, duration=15):
        """Renews the session"""
        if duration in self.ALLOWED_DURATIONS:
            if self.alive:
                self.end = datetime.now() + timedelta(minutes=duration)
                self.login = False
                return self.save()
            else:
                return False
        else:
            raise DurationOutOfBounds()

    def to_dict(self):
        """Converts the session to a dictionary"""
        return {
            'account': self.account.name,
            'token': self.token,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'login': True if self.login else False}


class CustomerSettings(HISModel):
    """Settings for a certain customer"""

    class Meta:
        db_table = 'customer_settings'

    customer = ForeignKeyField(Customer, db_column='customer')
    max_accounts = IntegerField(null=True, default=10)
    _logo = IntegerField(db_column='logo', null=True)
    logo = FileProperty(_logo, file_client)

    @classmethod
    def of(cls, customer):
        """Returns the settings of a respective customer"""
        return cls.get(cls.customer == customer)


tables = [Service, CustomerService, Account, AccountService, Session]
