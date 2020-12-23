"""HIS request context locals."""

from typing import Union

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from his.config import SESSION_ID, SESSION_SECRET
from his.exceptions import NoSessionSpecified, SessionExpired
from his.messages.account import NO_SUCH_ACCOUNT
from his.messages.account import NOT_AUTHORIZED
from his.messages.customer import NO_SUCH_CUSTOMER
from his.messages.data import INVALID_ACCOUNT_ID
from his.messages.data import INVALID_CUSTOMER_ID
from his.messages.data import MISSING_DATA
from his.orm import ALLOWED_SESSION_DURATIONS
from his.orm import DEFAULT_SESSION_DURATION
from his.orm import Account
from his.orm import Session


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER', 'JSON_DATA']


def get_session_id() -> int:
    """Returns the session ID."""

    try:
        ident = request.cookies[SESSION_ID]
    except KeyError:
        raise NoSessionSpecified() from None

    try:
        return int(ident)
    except ValueError:
        raise NoSessionSpecified() from None


def get_session_secret() -> str:
    """Returns the session secret."""

    try:
        return request.cookies[SESSION_SECRET]
    except KeyError:
        raise NoSessionSpecified() from None


def get_session() -> Session:
    """Returns the session from the cache."""

    ident = get_session_id()
    secret = get_session_secret()

    try:
        session = Session[ident]
    except Session.DoesNotExist:
        raise SessionExpired() from None

    if session.verify(secret):
        return session

    raise SessionExpired()


def get_account() -> Account:
    """Gets the verified targeted account."""

    try:
        aid = int(request.args['account'])
    except KeyError:
        return SESSION.account
    except (TypeError, ValueError):
        raise INVALID_ACCOUNT_ID from None

    if SESSION.account.root:
        try:
            return Account[aid]
        except Account.DoesNotExist:
            raise NO_SUCH_ACCOUNT from None

    if SESSION.account.admin:
        cid = SESSION.account.customer_id

        try:
            return Account.get((Account.id == aid) & (Account.customer == cid))
        except Account.DoesNotExist:
            raise NO_SUCH_ACCOUNT from None

    raise NOT_AUTHORIZED


def get_customer() -> Customer:
    """Gets the verified targeted customer."""

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return ACCOUNT.customer
    except (TypeError, ValueError):
        raise INVALID_CUSTOMER_ID from None

    if SESSION.account.root:
        try:
            return Customer.get(Customer.id == cid)
        except Customer.DoesNotExist:
            raise NO_SUCH_CUSTOMER from None

    raise NOT_AUTHORIZED


def get_session_duration() -> int:
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in ALLOWED_SESSION_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION


def get_json_data() -> Union[dict, list, int, float, str]:
    """Returns posted JSON data."""

    json = request.json

    if json is None:
        raise MISSING_DATA

    return json


class ModelProxy(LocalProxy):   # pylint: disable=R0903
    """Proxies ORM models."""

    def __int__(self):
        """Returns the primary key value."""
        return self.get_id()


SESSION = ModelProxy(get_session)
ACCOUNT = ModelProxy(get_account)
CUSTOMER = ModelProxy(get_customer)
JSON_DATA = LocalProxy(get_json_data)
