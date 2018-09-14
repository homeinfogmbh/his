"""Session cache server."""

from datetime import datetime, timedelta

from flask import request

from timelib import strpdatetime
from wsgilib import JSON

from his.application import Application
from his.cache.session import ServerCachedSession
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

        session = ServerCachedSession.from_record(record)
        self._sessions[session_token] = (datetime.now(), session)
        return session

    def get(self, session_token):
        """Returns the respective session."""
        try:
            cached, session = self._sessions[session_token]
        except KeyError:
            return self.reload(session_token)

        if datetime.now() - cached > INTERVAL or not session.alive:
            return self.reload(session_token)

        return session

    def refresh(self, session_token):
        """Refreshes the respective session."""
        session = self.get(session_token)
        record = session.record
        record.end = strpdatetime(request.json.pop('end'))
        record.login = request.json.pop('login', False)
        record.save()
        return self.reload(session_token)

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

    session = CACHE.refresh(session_token)
    return session.to_json()


@APPLICATION.route('/<session_token>', methods=['DELETE'])
def close_session(session_token):
    """Returns the respective session."""

    CACHE.close(session_token)
    return JSON({'closed': session_token})
