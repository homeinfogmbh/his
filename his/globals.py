"""HIS environment proxies, faking globals."""

from functools import lru_cache

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from his.messages import NoSuchAccount, AccountLocked, NotAuthorized, \
    NoSuchCustomer, InvalidCustomerID, NoSessionSpecified, NoSuchSession
from his.orm import Session, Account


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER']


@lru_cache()
def _get_session(session_token):
    """Returns the session or raises an error."""

    try:
        return Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise NoSuchSession()


def get_session():
    """Returns the session or raises an error."""

    try:
        session_token = request.args['session']
    except KeyError:
        raise NoSessionSpecified()

    return _get_session(session_token)


def get_account():
    """Gets the verified targeted account."""

    try:
        account = request.args['account']
    except KeyError:
        return Account.get(Account.id == SESSION.account_id)

    if SESSION.account.root:
        try:
            return Account.find(account)
        except Account.DoesNotExist:
            raise NoSuchAccount()
    elif SESSION.account.admin:
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

    if SESSION.account.root:
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
