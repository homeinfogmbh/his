"""HIS session service."""

from functools import wraps

from flask import request

from wsgilib import JSON

from his.api import authenticated
from his.cache.session import APICachedSession
from his.globals import ACCOUNT, SESSION, JSON_DATA
from his.messages.account import NotAuthorized
from his.messages.session import MissingCredentials, InvalidCredentials, \
    NoSuchSession
from his.orm import Account, Session

__all__ = ['ROUTES']


DURATION = 15


def _get_duration():
    """Returns the repsective session duration in minutes."""

    return int(request.args.get('duration', DURATION))


def _get_session_by_token(session_token):
    """Returns the respective session by the
    session token with authorization checks.
    """

    if session_token == '!':
        return SESSION

    session = APICachedSession.from_cache(session_token)
    conditions = (
        lambda: SESSION.token == session.token,
        lambda: ACCOUNT.root,
        lambda: ACCOUNT.admin and session.account.customer == ACCOUNT.customer)

    if any(condition() for condition in conditions):
        return session

    raise NoSuchSession()


def with_session(function):
    """Converts the first argument of function into a sesion."""

    @wraps(function)
    def wrapper(session_token, *args, **kwargs):
        return function(_get_session_by_token(session_token), *args, **kwargs)

    return wrapper


def login():
    """Opens a new session for the respective account."""

    account = JSON_DATA.get('account')
    passwd = JSON_DATA.get('passwd')

    if not account or not passwd:
        return MissingCredentials()

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return InvalidCredentials()

    if account.login(passwd):
        session = Session.open(account, duration=_get_duration())
        return JSON(session.to_json())

    return InvalidCredentials()


@authenticated
def list_():
    """Lists all sessions iff specified session is root."""

    if ACCOUNT.root:
        return JSON({session.token: session.to_json() for session in Session})

    if ACCOUNT.admin:
        return JSON({
            session.token: session.to_json() for session in
            Session.select().join(Account).where(
                Account.customer == ACCOUNT.customer)})

    return NotAuthorized()


@authenticated
@with_session
def get(session):
    """Lists the respective session."""

    return JSON(session.to_json())


@authenticated
@with_session
def refresh(session):
    """Refreshes an existing session."""

    session = session.renew(duration=_get_duration())
    return JSON(session.to_json())


@authenticated
@with_session
def close(session):
    """Closes the provided session."""

    session.close()
    return JSON({'closed': session.token})


ROUTES = (
    ('POST', '/session', login, 'login'),
    ('GET', '/session', list_, 'list_sessions'),
    ('GET', '/session/<session_token>', get, 'get_session'),
    ('PUT', '/session/<session_token>', refresh, 'refresh_session'),
    ('DELETE', '/session/<session_token>', close, 'close_session'))
