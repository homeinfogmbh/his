"""Customer <> Service mappings."""

from __future__ import annotations
from datetime import datetime
from typing import Optional, Union

from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect

from mdb import Company, Customer

from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ['CustomerService']


class CustomerService(HISModel):
    """Many-to-many Account <-> Services mapping."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_service'

    customer = ForeignKeyField(
        Customer, column_name='customer', backref='customer_services',
        on_delete='CASCADE', lazy_load=False)
    service = ForeignKeyField(
        Service, column_name='service', backref='customer_services',
        on_delete='CASCADE', lazy_load=False)
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
    def active(cls) -> ModelSelect:
        """Selects active customer services."""
        now = datetime.now()
        condition = (cls.start >> None) | (now >= cls.end)
        condition &= (cls.end >> None) | (now <= cls.end)
        return cls.select().where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects customer services."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, Service}
        return super().select(*args, **kwargs).join(Customer).join(
            Company).join_from(cls, Service)
