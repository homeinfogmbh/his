"""Chached sessions."""

from collections import namedtuple
from datetime import datetime, timedelta
from functools import lru_cache
from json import dumps
from uuid import UUID

from requests import get, patch, delete

from timelib import strpdatetime

from his.config import CONFIG
from his.messages.session import NoSuchSession, DurationOutOfBounds
from his.orm import Account, Session


__all__ = ['CachedSession']


class CachedSession(namedtuple('CachedSession', (
        'account_id', 'token', 'start', 'end', 'login'))):
    """A cached session."""

    def __str__(self):
        """Returns the respective JSON representation."""
        return dumps(self.to_json(), indent=2)

    @classmethod
    def from_record(cls, record):
        """Creates a cached session from the session database record."""
        return cls(
            record.account_id, record.token, record.start, record.end,
            record.login)

    @classmethod
    def from_cache(cls, session_token):
        """Returns the respective session from the cache."""
        response = get(CONFIG['cache']['url'].format(session_token))

        if response.status_code == 200:
            return cls.from_json(response.json())

        raise NoSuchSession()

    @classmethod
    def from_json(cls, json):
        """Creates a cached session from a JSON-ish dict."""
        account_id = json.pop('account')
        token = UUID(json.pop('token'))
        start = strpdatetime(json.pop('start'))
        end = strpdatetime(json.pop('end'))
        login = json.pop('login')
        return cls(account_id, token, start, end, login)

    @property
    @lru_cache()
    def account(self):
        """Returns the respective account."""
        return Account[self.account_id]

    @property
    def alive(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() < self.end

    @property
    def record(self):
        """Returns the appropriate record."""
        try:
            return Session.get(Session.token == self.token)
        except Session.DoesNotExist:
            raise NoSuchSession()

    @property
    def _url(self):
        """Returns the session cache server URL."""
        return CONFIG['cache']['url'].format(self.token)

    def _update(self, end, login):
        """Commits the current session data."""
        json = {'end': end.isoformat(), 'login': login}
        response = patch(self._url, json=json)
        return response.status_code == 200

    def close(self):
        """Closes the session."""
        response = delete(self._url)

        if response.status_code == 200:
            return True

        return False

    def renew(self, duration=15):
        """Renews the session."""
        if duration in Session.ALLOWED_DURATIONS:
            if self.alive:
                end = datetime.now() + timedelta(minutes=duration)
                return self._update(end, False)

            return False

        raise DurationOutOfBounds()

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'account': self.account_id,
            'token': self.token.hex,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'login': self.login}
