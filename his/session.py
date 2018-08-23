"""Chached sessions."""

from datetime import datetime, timedelta

from his.messages.session import NoSuchSession
from his.orm import Session


__all__ = ['SESSIONS']


TIMEOUT = 60    # Seconds.


class _SessionCache(dict):
    """Cached sessions."""

    def __new__(cls, timeout=TIMEOUT):
        """Creates a new session cache."""
        super().__new__(cls)

    def __init__(self, timeout):
        """Sets the respective timeout."""
        super().__init__()
        self.timeout = timeout
        self.last_refresh = None

    def __getitem__(self, session_token):
        """Returns the respective session."""
        if self.needs_reload:
            self.reload()

        try:
            session = super().__getitem__(session_token)
        except KeyError:
            reload = True
        else:
            reload = not session.alive

        if reload:
            try:
                session = Session.get(Session.token == session_token)
            except Session.DoesNotExist:
                raise NoSuchSession()

            self[session_token] = session

        return session

    @property
    def interval(self):
        """Returns the refresh interval."""
        return timedelta(seconds=self.timeout)

    @property
    def needs_reload(self):
        """Determines whether all sessions should be reloaded."""
        if self.last_refresh is None:
            return True

        return datetime.now() - self.last_refresh > self.interval

    def reload(self):
        """Reloads the session cache."""
        self.clear()

        for session in Session:
            self[session.token.hex] = session

        self.last_refresh = datetime.now()


SESSIONS = _SessionCache()
