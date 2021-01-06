"""Password reset."""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import DateTimeField
from peewee import ForeignKeyField
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
        on_delete='CASCADE')
    token = UUIDField(default=uuid4)
    created = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, account):
        """Adds a new password reset token."""
        try:
            record = cls.get(cls.account == account)
        except cls.DoesNotExist:
            record = cls()
            record.account = account
            return record

        if record.valid:
            raise PasswordResetPending()

        record.delete_instance()
        return cls.add(account)

    @property
    def valid(self) -> bool:
        """Determines whether the token is still valid."""
        return self.created + VALIDITY > datetime.now()
