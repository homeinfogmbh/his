"""HIS session service."""

from typing import Optional, Union

from flask import request, Response, make_response

from wsgilib import JSON, JSONMessage, require_json

from his.api import authenticated
from his.contextlocals import ACCOUNT, get_session_duration
from his.exceptions import InvalidCredentials, NotAuthorized
from his.functions import set_session_cookie, delete_session_cookie
from his.orm.account import Account
from his.orm.session import Session
from his.wsgi.functions import get_session


__all__ = ['ROUTES']


def make_login(account: Account, duration: int) -> Response:
    """Performs the actual login."""

    session, secret = Session.open(account, duration=duration)
    json = session.to_json()
    json['secret'] = secret
    response = JSON(json)
    return set_session_cookie(make_response(response), session, secret=secret)


@require_json(dict)
def login() -> Response:
    """Opens a new session for the respective account."""

    account = request.json['account']
    passwd = request.json['passwd']

    try:
        account = Account.select(cascade=True).where(
            Account.name == account
        ).get()
    except Account.DoesNotExist:
        raise InvalidCredentials() from None

    if account.login(passwd):
        return make_login(account, get_session_duration())

    raise InvalidCredentials()


@authenticated
def list_() -> Union[JSON, JSONMessage]:
    """Lists all sessions iff specified session is root."""

    select = Session.select().join(Account)

    if ACCOUNT.root:
        return JSON([session.to_json() for session in select.where(True)])

    condition = Account.customer == ACCOUNT.customer

    if ACCOUNT.admin:
        return JSON([session.to_json() for session in select.where(condition)])

    raise NotAuthorized()


@authenticated
def get(ident: Optional[int] = None) -> JSON:
    """Lists the respective session."""

    return JSON(get_session(ident).to_json())


@authenticated
def refresh(ident: Optional[int] = None) -> JSON:
    """Refreshes an existing session."""

    # Refresh is done by @authenricated automatically.
    return JSON(get_session(ident).to_json())


@authenticated
def close(ident: Optional[int] = None) -> Response:
    """Closes the provided session."""

    get_session(ident).delete_instance()
    return delete_session_cookie(make_response(JSON({'closed': ident})))


ROUTES = (
    ('POST', '/session', login),
    ('GET', '/session', list_),
    ('GET', '/session/<int:ident>', get),
    ('GET', '/session/!', lambda: get()),   # pylint: disable=W0108
    ('PUT', '/session/<int:ident>', refresh),
    ('PUT', '/session/!', lambda: refresh()),   # pylint: disable=W0108
    ('DELETE', '/session/<int:ident>', close),
    ('DELETE', '/session/!', lambda: close())   # pylint: disable=W0108
)
