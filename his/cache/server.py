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


class SessionCache(dict):
    """Cached sessions."""

    def __init__(self):
        """Sets the last refresh."""
        super().__init__()
        self.last_refresh = None

    def __getitem__(self, session_token):
        """Returns the respective session."""
        now = datetime.now()
        reload = False

        try:
            cached, cached_session = super().__getitem__(session_token)
        except KeyError:
            reload = True
        else:
            reload = now - cached > INTERVAL or not cached_session.alive

        if reload:
            try:
                record = Session.get(Session.token == session_token)
            except Session.DoesNotExist:
                raise NoSuchSession()

            if not record.alive:
                record.delete_instance()
                raise SessionExpired()

            cached_session = CachedSession.from_record(record)
            self[session_token] = (now, cached_session)

        return cached_session


CACHE = SessionCache()


@APPLICATION.route('/<session_token>', methods=['GET'])
def get_session(session_token):
    """Returns the respective session."""

    cached_session = CACHE[session_token]
    print('Cached session:', cached_session, flush=True)
    print('Cached session JSON:', cached_session.to_json(), flush=True)
    return JSON(CACHE[session_token].to_json())


@APPLICATION.route('/<session_token>', methods=['PATCH'])
def update_session(session_token):
    """Returns the respective session."""

    try:
        session = Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        return NoSuchSession()

    session.end = strpdatetime(request.json.pop('end'))
    session.login = request.json.pop('login', False)
    session.save()
    return 'Session updated.'


@APPLICATION.route('/<session_token>', methods=['DELETE'])
def close_session(session_token):
    """Returns the respective session."""

    with suppress(Session.DoesNotExist):
        Session.get(Session.token == session_token).delete_instance()

    with suppress(KeyError):
        CACHE.pop(session_token)

    return JSON({'closed': session_token})
