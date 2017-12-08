"""Customer-level meta services"""

from flask import jsonify
from peewee import DoesNotExist

from homeinfo.crm import Customer
from wsgilib import Binary

from his.api import authenticated
from his.globals import ACCOUNT, CUSTOMER, SU_CUSTOMER
from his.messages.account import NotAuthorized
from his.messages.customer import InvalidCustomerID, NoSuchCustomer, \
    CustomerUnconfigured
from his.orm import CustomerSettings

__all__ = ['get_customer', 'get_logo']


def customer_by_cid(cid):
    """Returns the customer by the respective customer ID."""

    try:
        cid = int(cid)
    except ValueError:
        raise InvalidCustomerID()

    try:
        return Customer.get(Customer.id == cid)
    except DoesNotExist:
        raise NoSuchCustomer()


def settings():
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == SU_CUSTOMER)
    except DoesNotExist:
        raise CustomerUnconfigured() from None


@authenticated
def get_customer(customer):
    """Allows services"""

    if customer == '!':
        return jsonify(CUSTOMER.to_dict())

    customer = customer_by_cid(customer)

    if ACCOUNT.root or CUSTOMER == customer:
        return jsonify(customer.to_dict())

    raise NotAuthorized()


@authenticated
def get_logo():
    """Allows services"""

    return Binary(settings().logo)
