"""HIS session service."""

from functools import wraps

from wsgilib import JSON

from his.api import authenticated
from his.contextlocals import ACCOUNT, SESSION, JSON_DATA, get_session_duration
from his.functions import set_session_cookie, delete_session_cookie
from his.messages.account import NOT_AUTHORIZED
from his.messages.session import INVALID_CREDENTIALS
from his.messages.session import MISSING_CREDENTIALS
from his.messages.session import NO_SUCH_SESSION
from his.orm import Account, Session


__all__ = ['ROUTES']


def _get_session_by_token(token):
    """Returns the respective session by the
    session token with authorization checks.
    """

    if token == '!':
        return SESSION

    session = Session.by_token(token)

    if session is None:
        return NO_SUCH_SESSION

    if SESSION.token == session.token:
        return session

    if ACCOUNT.root:
        return session

    if ACCOUNT.admin and session.account.customer == ACCOUNT.customer:
        return session

    raise NO_SUCH_SESSION


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
        return MISSING_CREDENTIALS

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return INVALID_CREDENTIALS

    if account.login(passwd):
        session, token = Session.open(account, duration=get_session_duration())
        json = session.to_json()
        json['token'] = token
        response = JSON(json)
        return set_session_cookie(response, session, token=token)

    return INVALID_CREDENTIALS


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

    return NOT_AUTHORIZED


@authenticated
@with_session
def get(session):
    """Lists the respective session."""

    return JSON(session.to_json())


@authenticated
@with_session
def refresh(session):
    """Refreshes an existing session."""

    # Refresh is done by @authenricated automatically.
    return JSON(session.to_json())


@authenticated
@with_session
def close(session):
    """Closes the provided session."""

    token = session.token.hex
    session.delete_instance()
    response = JSON({'closed': token})
    return delete_session_cookie(response)


ROUTES = (
    ('POST', '/session', login),
    ('GET', '/session', list_),
    ('GET', '/session/<session_token>', get),
    ('PUT', '/session/<session_token>', refresh),
    ('DELETE', '/session/<session_token>', close)
)
