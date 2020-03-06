"""A user session."""

from datetime import datetime, timedelta

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


__all__ = ['ALLOWED_SESSION_DURATIONS', 'DEFAULT_SESSION_DURATION', 'Session']


ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15


class Session(HISModel):
    """A session related to an account."""

    account = ForeignKeyField(
        Account, column_name='account', backref='sessions',
        on_delete='CASCADE')
    secret = Argon2Field()
    start = DateTimeField()
    end = DateTimeField()
    login = BooleanField(default=True)

    def __str__(self):
        """Returns a human-readable representation."""
        return '{} - {}: {} ({})'.format(
            self.start.isoformat(), self.end.isoformat(), self.id, self.login)

    @classmethod
    def add(cls, account, duration):
        """Actually opens a new login session."""
        now = datetime.now()
        session = cls()
        session.account = account
        session.secret = secret = genpw(length=32)
        session.start = now
        session.end = now + duration
        return (session, secret)

    @classmethod
    def open(cls, account, duration=DEFAULT_SESSION_DURATION):
        """Actually opens a new login session."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DURATION_OUT_OF_BOUNDS

        duration = timedelta(minutes=duration)
        session, secret = cls.add(account, duration)
        session.save()
        return (session, secret)

    @classmethod
    def cleanup(cls, before=None):
        """Cleans up orphaned sessions."""
        if before is None:
            before = datetime.now()

        for session in cls.select().where(cls.end < before):
            session.delete_instance()
            yield session

    @property
    def alive(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() < self.end

    def verify(self, secret):
        """Verifies the session."""
        try:
            if self.secret.verify(secret):  # pylint: disable=E1101
                return True
        except VerifyMismatchError:
            return False

        return False

    def renew(self, duration=DEFAULT_SESSION_DURATION):
        """Renews the session."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DURATION_OUT_OF_BOUNDS

        if not self.account.can_login:
            raise ACCOUNT_LOCKED

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self
