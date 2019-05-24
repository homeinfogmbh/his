"""Customer-level meta services."""

from mdb import Customer
from wsgilib import JSON, Binary

from his.api import authenticated, root
from his.contextlocals import ACCOUNT, CUSTOMER
from his.messages.customer import CUSTOMER_NOT_CONFIGURED, NO_SUCH_CUSTOMER
from his.messages.data import INVALID_CUSTOMER_ID
from his.orm import CustomerSettings


__all__ = ['get_customer', 'ROUTES']


def get_customer(name):
    """Returns the customer by the respective customer ID."""

    if name == '!':
        return CUSTOMER

    try:
        cid = int(name)
    except ValueError:
        raise INVALID_CUSTOMER_ID

    try:
        customer = Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise NO_SUCH_CUSTOMER

    conditions = (
        lambda: ACCOUNT.root,
        lambda: ACCOUNT.admin and customer == ACCOUNT.customer)

    if any(condition() for condition in conditions):
        return customer

    if customer.id == CUSTOMER.id:
        return CUSTOMER

    raise NO_SUCH_CUSTOMER


def _settings():
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == CUSTOMER)
    except CustomerSettings.DoesNotExist:
        raise CUSTOMER_NOT_CONFIGURED


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
    ('GET', '/customer', list_),
    ('GET', '/customer/<ident>', get),
    ('GET', '/customer-logo', get_logo)
)
