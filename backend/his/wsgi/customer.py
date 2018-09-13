"""Customer-level meta services."""

from mdb import Customer
from wsgilib import JSON, Binary

from his.api import authenticated, root
from his.globals import ACCOUNT, CUSTOMER
from his.messages.customer import NoSuchCustomer, CustomerUnconfigured
from his.messages.data import InvalidCustomerID
from his.orm import CustomerSettings

__all__ = ['get_customer', 'ROUTES']


def get_customer(name):
    """Returns the customer by the respective customer ID."""

    if name == '!':
        return CUSTOMER

    try:
        cid = int(name)
    except ValueError:
        raise InvalidCustomerID()

    try:
        customer = Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise NoSuchCustomer()

    conditions = (
        lambda: ACCOUNT.root,
        lambda: ACCOUNT.admin and customer == ACCOUNT.customer)

    if any(condition() for condition in conditions):
        return customer

    if customer.id == CUSTOMER.id:
        return CUSTOMER

    raise NoSuchCustomer()


def _settings():
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == CUSTOMER)
    except CustomerSettings.DoesNotExist:
        raise CustomerUnconfigured()


@authenticated
@root
def list_():
    """Lists available customers."""

    return JSON([customer.to_json(company=True) for customer in Customer])


@authenticated
def get(ident):
    """Allows services"""

    return JSON(get_customer(ident).to_json())


@authenticated
def get_logo():
    """Allows services"""

    return Binary(_settings().logo)


ROUTES = (
    ('GET', '/customer', list_, 'list_customers'),
    ('GET', '/customer/<ident>', get, 'get_customer'),
    ('GET', '/customer-logo', get_logo, 'get_customer_logo'))
