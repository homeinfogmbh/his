"""User sessions."""

from __future__ import annotations
from datetime import datetime, timedelta
from logging import getLogger
from typing import NamedTuple, Optional, Union

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Select

from mdb import Company, Customer
from peeweeplus import Argon2Field

from his.crypto import genpw
from his.exceptions import AccountLocked
from his.orm.account import Account
from his.orm.common import HISModel


__all__ = ["DURATION", "DURATION_RANGE", "Session"]


DURATION = 720
DURATION_RANGE = range(720)
LOGGER = getLogger("his.session")


class Session(HISModel):
    """A session related to an account."""

    account = ForeignKeyField(
        Account,
        column_name="account",
        backref="sessions",
        on_delete="CASCADE",
        lazy_load=False,
    )
    secret = Argon2Field()
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField(default=True)

    @classmethod
    def add(cls, account: Union[Account, int], duration: timedelta) -> NewSession:
        """Actually opens a new login session."""
        start = datetime.now()
        end = start + duration
        secret = genpw(length=32)
        session = cls(account=account, secret=secret, start=start, end=end)
        session.save()
        return NewSession(session=session, secret=secret)

    @classmethod
    def open(cls, account: Union[Account, int], duration: int = DURATION) -> NewSession:
        """Actually opens a new login session."""
        duration = timedelta(minutes=duration)
        session, secret = cls.add(account, duration)
        session.save()
        return NewSession(session=session, secret=secret)

    @classmethod
    def cleanup(cls, before: Optional[datetime] = None) -> int:
        """Cleans up orphaned sessions."""
        count = 0

        if before is None:
            before = datetime.now()

        sessions = cls.select().where(cls.end < before)

        for count, session in enumerate(sessions, start=1):
            session.delete_instance()
            LOGGER.info("Cleaned up session: %s", session)

        return count

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects sessions."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, Account, Customer, Company, *args})
            .join(Account)
            .join(Customer)
            .join(Company)
        )

    def verify(self, secret: str) -> bool:
        """Verifies the session."""
        try:
            return self.secret.verify(secret)
        except VerifyMismatchError:
            return False

    def renew(self, duration: int = DURATION) -> Session:
        """Renews the session."""
        if not self.account.can_login:
            raise AccountLocked()

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self


class NewSession(NamedTuple):
    """A new session, containing the
    session object and plain text secret.
    Discard this as soon as possible.
    """

    session: Session
    secret: str
