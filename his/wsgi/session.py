"""HIS session service."""

from json import loads

from flask import request, jsonify

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

    if SESSION.token == session.token:
        return session
    elif ACCOUNT.root:
        return session
    elif ACCOUNT.admin and session.account.customer == ACCOUNT.customer:
        return session

    raise NoSuchSession()


def login():
    """Opens a new session for the respective account."""

    json = loads(request.get_data().decode())
    account = json.get('account')
    passwd = json.get('passwd')

    if not account or not passwd:
        raise MissingCredentials()

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        raise InvalidCredentials()

    if account.login(passwd):
        session = Session.open(account, duration=_get_duration())
        return jsonify(session.to_dict())

    raise InvalidCredentials()


@authenticated
def list_():
    """Lists all sessions iff specified session is root."""

    if ACCOUNT.root:
        sessions = {session.token: session.to_dict() for session in Session}
        return jsonify(sessions)
    elif ACCOUNT.admin:
        sessions = {
            session.token: session.to_dict() for session in
            Session.select().join(Account).where(
                Account.customer == ACCOUNT.customer)}
        return jsonify(sessions)

    raise NotAuthorized()


@authenticated
def get(session_token):
    """Lists the respective session."""

    return jsonify(_get_session_by_token(session_token).to_dict())


@authenticated
def refresh(session_token):
    """Refreshes an existing session."""

    session = _get_session_by_token(session_token)

    if session.renew(duration=_get_duration()):
        return jsonify(session.to_dict())

    raise SessionExpired()


@authenticated
def close(session_token):
    """Tries to close a specific session identified by its token or
    all sessions for a certain account specified by its name.
    """

    session = _get_session_by_token(session_token)
    session.close()
    return jsonify({'closed': session.token})


ROUTES = (
    ('POST', '/session', login, 'login'),
    ('GET', '/session', list_, 'list_sessions'),
    ('GET', '/session/<session_token>', get, 'get_session'),
    ('PUT', '/session/<session_token>', refresh, 'refresh_session'),
    ('DELETE', '/session/<session_token>', close, 'close_session'))
