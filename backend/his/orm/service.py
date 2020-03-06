"""HIS services."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer

from his.exceptions import ServiceExistsError
from his.messages.service import SERVICE_LOCKED
from his.orm.account import Account
from his.orm.common import HISModel


__all__ = [
    'Service',
    'ServiceDependency',
    'ServiceDomain',
    'CustomerService',
    'AccountService'
]


class Service(HISModel):
    """Registers services of HIS."""

    name = CharField(32, null=True)
    description = CharField(255, null=True)
    # Flag whether the service shall be promoted.
    promote = BooleanField(default=True)
    # Flag whether the service is locked for maintenance.
    locked = BooleanField(default=False)

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

    @property
    def service_deps(self):
        """Yields dependencies of this service."""
        for service_dependency in self._service_deps:
            dependency = service_dependency.dependency
            yield dependency
            yield from dependency.service_deps

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

        if self.locked:
            raise SERVICE_LOCKED

        if self in CustomerService.services(account.customer):
            return account.admin or self in account.services

        return False


class ServiceDependency(HISModel):
    """Maps service dependencies."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_dependency'

    service = ForeignKeyField(
        Service, column_name='service', backref='_service_deps',
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
            service = customer_service.service
            yield service
            yield from service.service_deps

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
