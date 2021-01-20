"""Account <> Service mapping."""

from __future__ import annotations

from peewee import ForeignKeyField

from his.orm.account import Account
from his.orm.common import HISModel
from his.orm.customer_service import CustomerService
from his.orm.service import Service


__all__ = ['AccountService']


class AccountService(HISModel):
    """Many-to-many Account <-> Service mapping."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'account_service'

    account = ForeignKeyField(
        Account, column_name='account', backref='account_services',
        on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', backref='account_services',
        on_delete='CASCADE')

    def __str__(self):
        return f'{self.account}@{self.service}'

    @classmethod
    def add(cls, account: Account, service: Service) -> AccountService:
        """Adds a new account service."""
        try:
            return cls.get(account=account, service=service)
        except cls.DoesNotExist:
            record = cls(account=account, service=service)
            record.save()
            return record

    @classmethod
    def validate(cls, account: Account, service: Service) -> bool:
        """Checks whether the given account may use the given service."""
        if not CustomerService.validate(account.customer, service):
            return False

        try:
            return cls.get(account=account, service=service)
        except cls.DoesNotExist:
            return False
