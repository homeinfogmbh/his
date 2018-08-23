"""Chached sessions."""

from datetime import datetime, timedelta

from his.messages.session import NoSuchSession, SessionExpired
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
        now = datetime.now()
        reload = False

        try:
            cached, session = super().__getitem__(session_token)
        except KeyError:
            reload = True
        else:
            if now - cached > INTERVAL:
                reload = True
            elif not session.alive:
                reload = True

        if reload:
            try:
                session = Session.get(Session.token == session_token)
            except Session.DoesNotExist:
                raise NoSuchSession()

            if not session.alive:
                raise SessionExpired()

            self[session_token] = (now, session)

        return session


SESSIONS = _SessionCache()
