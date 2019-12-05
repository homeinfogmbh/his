"""HIS request context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from his.config import COOKIE
from his.exceptions import NoSessionSpecified, SessionExpired
from his.messages.account import NO_SUCH_ACCOUNT
from his.messages.account import NOT_AUTHORIZED
from his.messages.customer import NO_SUCH_CUSTOMER
from his.messages.data import INVALID_ACCOUNT_ID
from his.messages.data import INVALID_CUSTOMER_ID
from his.messages.data import MISSING_DATA
from his.orm import DEFAULT_SESSION_DURATION, Account, Session


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER', 'JSON_DATA']


def get_session():
    """Returns the session from the cache."""

    try:
        session_token = request.cookies[COOKIE]
    except KeyError:
        raise NoSessionSpecified()

    try:
        session_token = UUID(session_token)
    except ValueError:
        raise SessionExpired()

    try:
        return Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise SessionExpired()


def get_account():
    """Gets the verified targeted account."""

    try:
        aid = int(request.args['account'])
    except KeyError:
        return SESSION.account
    except (TypeError, ValueError):
        raise INVALID_ACCOUNT_ID

    if SESSION.account.root:
        try:
            return Account[aid]
        except Account.DoesNotExist:
            raise NO_SUCH_ACCOUNT

    if SESSION.account.admin:
        cid = SESSION.account.customer_id

        try:
            return Account.get((Account.id == aid) & (Account.customer == cid))
        except Account.DoesNotExist:
            raise NO_SUCH_ACCOUNT

    raise NOT_AUTHORIZED


def get_customer():
    """Gets the verified targeted customer."""

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return ACCOUNT.customer
    except (TypeError, ValueError):
        raise INVALID_CUSTOMER_ID

    if SESSION.account.root:
        try:
            return Customer.get(Customer.id == cid)
        except Customer.DoesNotExist:
            raise NO_SUCH_CUSTOMER

    raise NOT_AUTHORIZED


def get_session_duration():
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in Session.ALLOWED_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION


def get_json_data():
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
