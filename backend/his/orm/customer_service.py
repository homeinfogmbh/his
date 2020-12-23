"""Customer <> Service mappings."""

from datetime import datetime
from typing import Iterator, Union

from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer

from his.orm.account_service import AccountService
from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ['CustomerService']


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_service'

    customer = ForeignKeyField(
        Customer, column_name='customer', backref='customer_services',
        on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', backref='customer_services',
        on_delete='CASCADE')
    begin = DateTimeField(null=True)
    end = DateTimeField(null=True)

    def __str__(self):
        return f'{self.customer_id}@{self.service}'

    @classmethod
    def add(cls, customer: Union[Customer, int], service: Union[Service, int],
            begin: datetime = None, end: datetime = None):
        """Adds a new customer service."""
        customer_service = cls()
        customer_service.customer = customer
        customer_service.service = service
        customer_service.begin = begin
        customer_service.end = end
        return customer_service

    @classmethod
    def services(cls, customer: Customer) -> Iterator[Service]:
        """Yields services for the respective customer."""
        for customer_service in cls.select().where(cls.customer == customer):
            yield customer_service.service

            for service in customer_service.service.service_deps:
                yield service

    @property
    def active(self) -> bool:
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
