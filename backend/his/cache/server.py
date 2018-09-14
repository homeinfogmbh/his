"""Session cache server."""

from contextlib import suppress
from datetime import datetime, timedelta

from flask import request

from timelib import strpdatetime
from wsgilib import JSON

from his.application import Application
from his.cache.session import CachedSession
from his.messages.session import NoSuchSession, SessionExpired
from his.orm import Session


__all__ = ['APPLICATION']


INTERVAL = timedelta(seconds=60)
APPLICATION = Application('SessionCacheServer')


class SessionCache:
    """Cached sessions."""

    def __init__(self):
        """Sets the last refresh."""
        self._sessions = {}

    def reload(self, session_token):
        """Updates the respective session."""
        try:
            record = Session.get(Session.token == session_token)
        except Session.DoesNotExist:
            raise NoSuchSession()

        if not record.alive:
            record.delete_instance()
            raise SessionExpired()

        cached_session = CachedSession.from_record(record)
        self._sessions[session_token] = (datetime.now(), cached_session)
        return cached_session

    def get(self, session_token):
        """Returns the respective session."""
        try:
            cached, cached_session = self._sessions[session_token]
        except KeyError:
            return self.reload(session_token)

        if datetime.now() - cached > INTERVAL or not cached_session.alive:
            return self.reload(session_token)

        return cached_session

    def close(self, session_token):
        """Closes the respective session."""
        try:
            record = Session.get(Session.token == session_token)
        except Session.DoesNotExist:
            self._sessions.pop(session_token, None)
            return

        record.delete_instance()
        self._sessions.pop(session_token, None)


CACHE = SessionCache()


@APPLICATION.route('/<session_token>', methods=['GET'])
def get_session(session_token):
    """Returns the respective session."""

    return JSON(CACHE.get(session_token).to_json())


@APPLICATION.route('/<session_token>', methods=['PATCH'])
def update_session(session_token):
    """Returns the respective session."""

    session = CACHE.get(session_token)
    record = session.record
    record.end = strpdatetime(request.json.pop('end'))
    record.login = request.json.pop('login', False)
    record.save()
    session = CACHE.reload(session_token)   # Force re-cache.
    return session.to_json()


@APPLICATION.route('/<session_token>', methods=['DELETE'])
def close_session(session_token):
    """Returns the respective session."""

    with suppress(Session.DoesNotExist):
        Session.get(Session.token == session_token).delete_instance()

    CACHE.close(session_token)
    return JSON({'closed': session_token})
