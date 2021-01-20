"""Password reset."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect
from peewee import UUIDField

from his.exceptions import PasswordResetPending
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
            record = cls.get(cls.account == account)
        except cls.DoesNotExist:
            record = cls(account=account)
            record.save()
            return record

        if record.valid:
            raise PasswordResetPending()

        record.delete_instance()
        return cls.add(account)

    @classmethod
    def active(cls) -> ModelSelect:
        """Selects active tokens."""
        select = cls.select(cls, Account).join(Account)
        condition = cls.created > (datetime.now() - VALIDITY)
        return select.where(condition)
