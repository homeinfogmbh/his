"""HIS environment proxies, faking globals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from his.messages import NoSuchAccount, AccountLocked, NotAuthorized, \
    NoSuchCustomer, InvalidCustomerID, NoSessionSpecified, NoSuchSession, \
    InvalidUUID
from his.orm import Session, Account
from his.request import REQUEST_GROUPS


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER']


def _get_session():
    """Returns the session from the database."""

    try:
        session_token = request.args['session']
    except KeyError:
        raise NoSessionSpecified()

    try:
        return Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise NoSuchSession()


def _get_request_group_session():
    """Returns the session of the respective request group."""

    try:
        request_group_token = UUID(request.args['request_group'])
    except (TypeError, ValueError):
        raise InvalidUUID()

    return REQUEST_GROUPS.get_session(request_group_token)


def get_session():
    """Returns the session or raises an error."""

    try:
        return _get_request_group_session()
    except KeyError:
        return _get_session()


def get_account():
    """Gets the verified targeted account."""

    try:
        account = request.args['account']
    except KeyError:
        return SESSION.live_account

    if SESSION.live_account.root:
        try:
            return Account.find(account)
        except Account.DoesNotExist:
            raise NoSuchAccount()
    elif SESSION.live_account.admin:
        try:
            account = Account.find(account, customer=CUSTOMER.id)
        except Account.DoesNotExist:
            raise NoSuchAccount()

        if account.usable:
            return account

        raise AccountLocked()

    raise NotAuthorized()


def get_customer():
    """Gets the verified targeted customer."""

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return ACCOUNT.customer
    except (TypeError, ValueError):
        raise InvalidCustomerID()

    if SESSION.live_account.root:
        try:
            return Customer.get(Customer.id == cid)
        except Customer.DoesNotExist:
            raise NoSuchCustomer()

    raise NotAuthorized()


class ModelProxy(LocalProxy):
    """Proxies ORM models."""

    def __int__(self):
        """Returns the primary key value."""
        return self._get_current_object().get_id()


SESSION = ModelProxy(get_session)
ACCOUNT = ModelProxy(get_account)
CUSTOMER = ModelProxy(get_customer)
