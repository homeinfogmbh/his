"""HIS environment proxies, faking globals."""

from logging import getLogger
from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from his.messages.account import AccountLocked
from his.messages.account import NoSuchAccount
from his.messages.account import NotAuthorized
from his.messages.customer import NoSuchCustomer
from his.messages.data import InvalidCustomerID
from his.messages.data import MissingData
from his.messages.session import NoSessionSpecified, NoSuchSession
from his.orm import Account, Session


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER', 'JSON_DATA']


LOGGER = getLogger(__file__)


def _get_substituted_account(account_name):
    """Returns the respective substituted account."""

    session_account = SESSION.account

    if not session_account.usable:
        raise AccountLocked()

    if session_account.root:
        try:
            return Account.find(account_name)
        except Account.DoesNotExist:
            raise NoSuchAccount()
    elif session_account.admin:
        try:
            return Account.find(account_name, customer=CUSTOMER.id)
        except Account.DoesNotExist:
            raise NoSuchAccount()

    raise NotAuthorized()


def get_session():
    """Returns the session from the cache."""

    try:
        session_token = request.cookies['session']
    except KeyError:
        try:
            session_token = request.args['session']
        except KeyError:
            raise NoSessionSpecified()

    try:
        session_token = UUID(session_token)
    except ValueError:
        raise NoSuchSession()

    try:
        return Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise NoSuchSession()


def get_account():
    """Gets the verified targeted account."""

    try:
        account_name = request.args['account']
    except KeyError:
        account = SESSION.account

        if account.usable:
            return account

        raise AccountLocked()

    return _get_substituted_account(account_name)


def get_customer():
    """Gets the verified targeted customer."""

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return ACCOUNT.customer
    except (TypeError, ValueError):
        raise InvalidCustomerID()

    if SESSION.account.root:
        try:
            return Customer.get(Customer.id == cid)
        except Customer.DoesNotExist:
            raise NoSuchCustomer()

    raise NotAuthorized()


def get_json_data():
    """Returns posted JSON data."""

    json = request.json

    if json is None:
        raise MissingData()

    return json


class ModelProxy(LocalProxy):
    """Proxies ORM models."""

    def __int__(self):
        """Returns the primary key value."""
        return self._get_current_object().get_id()


SESSION = ModelProxy(get_session)
ACCOUNT = ModelProxy(get_account)
CUSTOMER = ModelProxy(get_customer)
JSON_DATA = LocalProxy(get_json_data)
