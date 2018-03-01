"""Customer-level meta services"""

from flask import jsonify

from homeinfo.crm import Customer
from wsgilib import Binary

from his.api import authenticated
from his.globals import ACCOUNT, CUSTOMER
from his.messages.account import NotAuthorized
from his.messages.customer import NoSuchCustomer, CustomerUnconfigured
from his.messages.data import InvalidCustomerID
from his.orm import CustomerSettings

__all__ = ['ROUTES']


def customer_by_name(name):
    """Returns the customer by the respective customer ID."""

    if name == '!':
        return CUSTOMER

    try:
        cid = int(name)
    except ValueError:
        raise InvalidCustomerID()

    return Customer.get(Customer.id == cid)


def settings():
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == CUSTOMER)
    except CustomerSettings.DoesNotExist:
        raise CustomerUnconfigured() from None


@authenticated
def get(ident):
    """Allows services"""

    if ACCOUNT.root:
        try:
            customer = customer_by_name(ident)
        except Customer.DoesNotExist:
            raise NoSuchCustomer()
    elif ACCOUNT.admin:
        try:
            customer = customer_by_name(ident)
        except Customer.DoesNotExist:
            raise NotAuthorized()

        if CUSTOMER == customer:
            return jsonify(customer.to_dict())

    raise NotAuthorized()


@authenticated
def get_logo():
    """Allows services"""

    return Binary(settings().logo)


ROUTES = (
    ('GET', '/customer/<ident>', get, 'get_customer'),
    ('GET', '/customer-logo', get_logo, 'get_customer_logo'))
