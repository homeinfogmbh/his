"""Customer <> Service mappings."""

from __future__ import annotations
from datetime import datetime
from typing import Optional, Union

from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer

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
            begin: Optional[datetime] = None,
            end: Optional[datetime] = None) -> CustomerService:
        """Adds a new customer service."""
        try:
            record = cls.get(customer=customer, service=service)
        except cls.DoesNotExist:
            record = cls(customer=customer, service=service)

        record.begin = begin
        record.end = end
        record.save()
        return record

    @classmethod
    def validate(cls, customer: Union[Customer, int],
                 service: Union[Service, int]) -> bool:
        """Checks whether the given customer may use the given service."""
        try:
            return cls.get(customer=customer, service=service).active
        except cls.DoesNotExist:
            return False

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
