"""Session cache server."""

from datetime import datetime, timedelta
from functools import wraps
from uuid import UUID

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


def with_uuid(function):
    """Converts the first argument into a UUID."""

    @wraps(function)
    def wrapper(token, *args, **kwargs):
        return function(UUID(token), *args, **kwargs)

    return wrapper


class SessionCache:
    """Cached sessions."""

    def __init__(self):
        """Sets the last refresh."""
        self._sessions = {}

    def reload(self, token):
        """Updates the respective session from the database."""
        try:
            record = Session.get(Session.token == token)
        except Session.DoesNotExist:
            raise NoSuchSession()

        if not record.alive:
            record.delete_instance()
            raise SessionExpired()

        session = ServerCachedSession.from_record(record)
        self._sessions[token] = (datetime.now(), session)
        return session

    def get(self, token):
        """Returns the respective session."""
        try:
            cached, session = self._sessions[token]
        except KeyError:
            return self.reload(token)

        if datetime.now() - cached > INTERVAL or not session.alive:
            return self.reload(token)

        return session

    def refresh(self, token):
        """Refreshes the respective session."""
        session = self.get(token)
        record = session.record
        record.end = strpdatetime(request.json.pop('end'))
        record.login = request.json.pop('login', False)
        record.save()
        return self.reload(token)

    def close(self, token):
        """Closes the respective session."""
        try:
            record = Session.get(Session.token == token)
        except Session.DoesNotExist:
            self._sessions.pop(token, None)
            return

        record.delete_instance()
        self._sessions.pop(token, None)


CACHE = SessionCache()


@APPLICATION.route('/<token>', methods=['GET'])
@with_uuid
def get_session(token):
    """Returns the respective session."""

    session = CACHE.get(token)
    return JSON(session.to_json())


@APPLICATION.route('/<token>', methods=['PATCH'])
@with_uuid
def update_session(token):
    """Returns the respective session."""

    session = CACHE.refresh(token)
    return session.to_json()


@APPLICATION.route('/<token>', methods=['DELETE'])
@with_uuid
def close_session(token):
    """Returns the respective session."""

    CACHE.close(token)
    return JSON({'closed': token.hex})
