"""Account <> Service mapping."""

from peewee import ForeignKeyField

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
        on_delete='CASCADE')
    service = ForeignKeyField(
        Service, column_name='service', backref='account_services',
        on_delete='CASCADE')

    def __str__(self):
        return f'{self.account}@{self.service}'

    @classmethod
    def add(cls, account, service):
        """Adds a new account service."""
        return cls(account=account, service=service)
