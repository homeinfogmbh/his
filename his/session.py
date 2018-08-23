"""Chached sessions."""

from datetime import datetime, timedelta

from his.messages.session import NoSuchSession
from his.orm import Session


__all__ = ['SESSIONS']


INTERVAL = timedelta(seconds=60)


class _SessionCache(dict):
    """Cached sessions."""

    def __new__(cls):
        """Creates a new session cache."""
        return super().__new__(cls)

    def __init__(self):
        """Sets the last refresh."""
        super().__init__()
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
    def needs_reload(self):
        """Determines whether all sessions should be reloaded."""
        if self.last_refresh is None:
            return True

        return datetime.now() - self.last_refresh > INTERVAL

    def reload(self):
        """Reloads the session cache."""
        self.clear()

        for session in Session:
            if session.alive:
                self[session.token.hex] = session
            else:
                session.delete_instance()

        self.last_refresh = datetime.now()


SESSIONS = _SessionCache()
