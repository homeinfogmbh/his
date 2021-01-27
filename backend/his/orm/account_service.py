"""Account <> Service mapping."""

from __future__ import annotations
from typing import Union

from peewee import ForeignKeyField, ModelSelect

from mdb import Company, Customer

from his.orm.account import Account
from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ['AccountService']


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'account_service'

    account = ForeignKeyField(
        Account, column_name='account', backref='account_services',
        on_delete='CASCADE', lazy_load=False)
    service = ForeignKeyField(
        Service, column_name='service', backref='account_services',
        on_delete='CASCADE', lazy_load=False)

    def __str__(self):
        return f'{self.account}@{self.service}'

    @classmethod
    def add(cls, account: Union[Account, int],
            service: [Service, int]) -> AccountService:
        """Adds a new account service."""
        try:
            return cls.get(account=account, service=service)
        except cls.DoesNotExist:
            record = cls(account=account, service=service)
            record.save()
            return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects account services."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Account, Customer, Company, Service}
        return super().select(*args, **kwargs).join(Account).join(
            Customer).join(Company).join_from(cls, Service)
