"""HIS session service."""

from typing import Union

from flask import request

from wsgilib import JSON, JSONMessage

from his.api import authenticated
from his.contextlocals import ACCOUNT, get_session_duration
from his.exceptions import InvalidCredentials, NotAuthorized
from his.functions import set_session_cookie, delete_session_cookie
from his.orm.account import Account
from his.orm.session import Session
from his.wsgi.decorators import require_json, with_session


__all__ = ['ROUTES']


@require_json(dict)
def login() -> Union[JSON, JSONMessage]:
    """Opens a new session for the respective account."""

    account = request.json['account']
    passwd = request.json['passwd']

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        raise InvalidCredentials() from None

    if account.login(passwd):
        session, secret = Session.open(
            account, duration=get_session_duration())
        json = session.to_json()
        json['secret'] = secret
        response = JSON(json)
        return set_session_cookie(response, session, secret=secret)

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
