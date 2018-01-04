"""HIS environment proxies, faking globals."""

from flask import request
from peewee import DoesNotExist
from werkzeug.local import LocalProxy

from homeinfo.crm import Customer

from his.messages.account import NoSuchAccount, NotAuthorized
from his.messages.customer import InvalidCustomerID, NoSuchCustomer
from his.messages.session import NoSessionSpecified, NoSuchSession
from his.orm import Session, Account


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER', 'SU_ACCOUNT', 'SU_CUSTOMER']


def get_session():
    """Returns the session or raises an error."""

    try:
        session_token = request.args['session']
    except KeyError:
        raise NoSessionSpecified()

    try:
        return Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()


def get_account():
    """Gets the verified targeted account."""

    try:
        su_account = request.args['account']
    except KeyError:
        return ACCOUNT

    if ACCOUNT.root or ACCOUNT.admin:
        try:
            su_account = Account.find(su_account)
        except DoesNotExist:
            raise NoSuchAccount()

        if ACCOUNT.root:
            return su_account
        elif ACCOUNT.admin and su_account.customer == CUSTOMER.id:
            return su_account

    raise NotAuthorized()


def get_customer():
    """Gets the verified targeted customer."""

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return CUSTOMER
    except (TypeError, ValueError):
        raise InvalidCustomerID()

    if ACCOUNT.root:
        try:
            return Customer.get(Customer.id == cid)
        except DoesNotExist:
            raise NoSuchCustomer()

    raise NotAuthorized()


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(lambda: SESSION.account)
CUSTOMER = LocalProxy(lambda: ACCOUNT.customer)
SU_ACCOUNT = LocalProxy(get_account)
SU_CUSTOMER = LocalProxy(get_customer)
