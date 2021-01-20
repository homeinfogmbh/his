"""HIS session service."""

from functools import wraps
from typing import Callable, Union

from wsgilib import JSON, JSONMessage

from his.api import authenticated
from his.contextlocals import ACCOUNT, SESSION, get_session_duration
from his.decorators import require_json
from his.functions import set_session_cookie, delete_session_cookie
from his.orm import Account, Session
from his.wsgi.functions import get_session


__all__ = ['ROUTES']


def with_session(function: Callable) -> Callable:
    """Converts the first argument of function into a sesion."""

    @wraps(function)
    def wrapper(ident: str, *args, **kwargs):
        return function(get_session(ident), *args, **kwargs)

    return wrapper


@require_json(dict)
def login() -> Union[JSON, JSONMessage]:
    """Opens a new session for the respective account."""

    account = JSON_DATA.get('account')
    passwd = JSON_DATA.get('passwd')

    if not account or not passwd:
        return MISSING_CREDENTIALS

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return INVALID_CREDENTIALS

    duration = get_session_duration()

    if account.login(passwd):
        session, secret = Session.open(account, duration=duration)
        json = session.to_json()
        json['secret'] = secret
        response = JSON(json)
        return set_session_cookie(response, session, secret=secret)

    return INVALID_CREDENTIALS


@authenticated
def list_() -> Union[JSON, JSONMessage]:
    """Lists all sessions iff specified session is root."""

    if ACCOUNT.root:
        return JSON({session.id: session.to_json() for session in Session})

    if ACCOUNT.admin:
        return JSON({
            session.id: session.to_json() for session in
            Session.select().join(Account).where(
                Account.customer == ACCOUNT.customer)})

    return NOT_AUTHORIZED


@authenticated
@with_session
def get(session) -> JSON:
    """Lists the respective session."""

    return JSON(session.to_json())


@authenticated
@with_session
def refresh(session: Session) -> JSON:
    """Refreshes an existing session."""

    # Refresh is done by @authenricated automatically.
    return JSON(session.to_json())


@authenticated
@with_session
def close(session: Session) -> JSON:
    """Closes the provided session."""

    ident = session.id
    session.delete_instance()
    response = JSON({'closed': ident})
    return delete_session_cookie(response)


ROUTES = (
    ('POST', '/session', login),
    ('GET', '/session', list_),
    ('GET', '/session/<ident>', get),
    ('PUT', '/session/<ident>', refresh),
    ('DELETE', '/session/<ident>', close)
)
