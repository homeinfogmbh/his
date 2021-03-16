"""Password reset."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from peewee import JOIN
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect
from peewee import UUIDField

from mdb import Address, Company, Customer

from his.orm.account import Account
from his.orm.common import HISModel


__all__ = ['VALIDITY', 'PasswordResetToken']


VALIDITY = timedelta(hours=1)


class PasswordResetToken(HISModel):
    """Tokens to reset passwords."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'password_reset_token'

    account = ForeignKeyField(
        Account, column_name='account', backref='password_reset_tokens',
        on_delete='CASCADE', lazy_load=False)
    token = UUIDField(default=uuid4)
    created = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, account: Union[Account, int]) -> PasswordResetToken:
        """Adds a new password reset token."""
        try:
            return cls.active().where(cls.account == account).get()
        except cls.DoesNotExist:
            record = cls(account=account)
            record.save()
            return record

    @classmethod
    def active(cls) -> ModelSelect:
        """Selects active tokens."""
        condition = cls.created > (datetime.now() - VALIDITY)
        return cls.select(cascade=True).where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects records."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Account, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(Account).join(
            Customer).join(Company).join(Address, join_type=JOIN.LEFT_OUTER)
