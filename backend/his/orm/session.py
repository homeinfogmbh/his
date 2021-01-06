"""User sessions."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterator

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField

from peeweeplus import Argon2Field

from his.crypto import genpw
from his.messages.account import ACCOUNT_LOCKED
from his.messages.session import DURATION_OUT_OF_BOUNDS
from his.orm.account import Account
from his.orm.common import HISModel


__all__ = ['DURATION', 'DURATION_RANGE', 'Session']


DURATION = 15
DURATION_RANGE = range(120)


class Session(HISModel):
    """A session related to an account."""

    account = ForeignKeyField(
        Account, column_name='account', backref='sessions',
        on_delete='CASCADE')
    secret = Argon2Field()
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField(default=True)

    @classmethod
    def add(cls, account: Account, duration: timedelta) -> Session:
        """Actually opens a new login session."""
        now = datetime.now()
        session = cls()
        session.account = account
        session.secret = secret = genpw(length=32)
        session.start = now
        session.end = now + duration
        return (session, secret)

    @classmethod
    def open(cls, account: Account, duration: int = DURATION) -> Session:
        """Actually opens a new login session."""
        if duration not in DURATION_RANGE:
            raise DURATION_OUT_OF_BOUNDS

        duration = timedelta(minutes=duration)
        session, secret = cls.add(account, duration)
        session.save()
        return (session, secret)

    @classmethod
    def cleanup(cls, before: datetime = None) -> Iterator[Session]:
        """Cleans up orphaned sessions."""
        if before is None:
            before = datetime.now()

        for session in cls.select().where(cls.end < before):
            session.delete_instance()
            yield session

    @property
    def alive(self) -> bool:
        """Determines whether the session is active."""
        return self.start <= datetime.now() < self.end

    def verify(self, secret: str) -> bool:
        """Verifies the session."""
        try:
            if self.secret.verify(secret):  # pylint: disable=E1101
                return True
        except VerifyMismatchError:
            return False

        return False

    def renew(self, duration: int = DURATION) -> Session:
        """Renews the session."""
        if duration not in DURATION_RANGE:
            raise DURATION_OUT_OF_BOUNDS

        if not self.account.can_login:
            raise ACCOUNT_LOCKED

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self
