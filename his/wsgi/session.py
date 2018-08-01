"""HIS session service."""

from flask import request

from wsgilib import JSON

from his.api import authenticated
from his.globals import ACCOUNT, SESSION
from his.messages.account import NotAuthorized
from his.messages.session import MissingCredentials, InvalidCredentials, \
    NoSuchSession, SessionExpired
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

    try:
        session = Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise NoSuchSession()

    conditions = (
        lambda: SESSION.token == session.token,
        lambda: ACCOUNT.root,
        lambda: ACCOUNT.admin and session.account.customer == ACCOUNT.customer)

    if any(condition() for condition in conditions):
        return session

    raise NoSuchSession()


def login():
    """Opens a new session for the respective account."""

    account = request.json.get('account')
    passwd = request.json.get('passwd')

    if not account or not passwd:
        raise MissingCredentials()

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        raise InvalidCredentials()

    if account.login(passwd):
        session = Session.open(account, duration=_get_duration())
        return JSON(session.to_dict())

    raise InvalidCredentials()


@authenticated
def list_():
    """Lists all sessions iff specified session is root."""

    if ACCOUNT.root:
        return JSON({session.token: session.to_dict() for session in Session})

    if ACCOUNT.admin:
        return JSON({
            session.token: session.to_dict() for session in
            Session.select().join(Account).where(
                Account.customer == ACCOUNT.customer)})

    raise NotAuthorized()


@authenticated
def get(session_token):
    """Lists the respective session."""

    return JSON(_get_session_by_token(session_token).to_dict())


@authenticated
def refresh(session_token):
    """Refreshes an existing session."""

    session = _get_session_by_token(session_token)

    if session.renew(duration=_get_duration()):
        return JSON(session.to_dict())

    raise SessionExpired()


@authenticated
def close(session_token):
    """Closes the provided session."""

    session = _get_session_by_token(session_token)
    session.close()
    return JSON({'closed': session.token})


ROUTES = (
    ('POST', '/session', login, 'login'),
    ('GET', '/session', list_, 'list_sessions'),
    ('GET', '/session/<session_token>', get, 'get_session'),
    ('PUT', '/session/<session_token>', refresh, 'refresh_session'),
    ('DELETE', '/session/<session_token>', close, 'close_session'))
