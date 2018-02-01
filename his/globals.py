"""HIS environment proxies, faking globals."""

from flask import request
from werkzeug.local import LocalProxy

from homeinfo.crm import Customer

from his.messages import NoSuchAccount, NotAuthorized, NoSuchCustomer, \
    InvalidCustomerID, NoSessionSpecified, NoSuchSession
from his.orm import Session, Account


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER']


def get_session():
    """Returns the session or raises an error."""

    try:
        session_token = request.args['session']
    except KeyError:
        raise NoSessionSpecified()

    try:
        return Session.get(Session.token == session_token)
    except Session.DoesNotExist:
        raise NoSuchSession()


def get_account():
    """Gets the verified targeted account."""

    try:
        account = request.args['account']
    except KeyError:
        return SESSION.account

    if SESSION.account.root or SESSION.account.admin:
        try:
            account = Account.find(account)
        except Account.DoesNotExist:
            raise NoSuchAccount()

        if SESSION.account.root:
            return account
        elif SESSION.account.admin and account.customer == CUSTOMER.id:
            return account

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
        return self._get_current_object()._get_pk_value()


SESSION = ModelProxy(get_session)
ACCOUNT = ModelProxy(get_account)
CUSTOMER = ModelProxy(get_customer)
