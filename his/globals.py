"""HIS environment globals."""

from flask import request
from peewee import DoesNotExist
from werkzeug.local import LocalProxy

from homeinfo.crm import Customer

from his.messages.account import NoSuchAccount, NotAuthorized
from his.messages.customer import InvalidCustomerID, NoSuchCustomer
from his.messages.session import NoSessionSpecified, NoSuchSession
from his.orm import Session, Account


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER']


def get_session():
    """Returns the session or raises an error."""

    try:
        session_token = request.args['session']
    except KeyError:
        raise NoSessionSpecified() from None

    try:
        return Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession() from None


def get_account():
    """Gets the verified targeted account."""

    session_account = SESSION.account

    try:
        su_account = request.args['account']
    except KeyError:
        return session_account

    if session_account.root or session_account.admin:
        try:
            su_account = Account.find(su_account)
        except DoesNotExist:
            raise NoSuchAccount() from None

        if session_account.root:
            return su_account
        elif session_account.admin:
            if session_account.customer == su_account.customer:
                return su_account

    raise NotAuthorized() from None


def get_customer():
    """Gets the verified targeted customer."""

    session_account = SESSION.account

    try:
        cid = int(request.args['customer'])
    except KeyError:
        return session_account.customer
    except (TypeError, ValueError):
        raise InvalidCustomerID() from None

    if session_account.root:
        try:
            return Customer.get(Customer.id == cid)
        except DoesNotExist:
            raise NoSuchCustomer() from None

    raise NotAuthorized() from None


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(get_account)
CUSTOMER = LocalProxy(get_customer)
