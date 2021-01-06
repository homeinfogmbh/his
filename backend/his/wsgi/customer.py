"""Customer-level meta services."""

from mdb import Customer
from wsgilib import JSON, Binary

from his.api import authenticated, root
from his.contextlocals import ACCOUNT, CUSTOMER
from his.messages.customer import CUSTOMER_NOT_CONFIGURED, NO_SUCH_CUSTOMER
from his.messages.data import INVALID_CUSTOMER_ID
from his.orm import CustomerSettings


__all__ = ['get_customer', 'ROUTES']


def get_customer(name: str) -> Customer:
    """Returns the customer by the respective customer ID."""

    if name == '!':
        return CUSTOMER

    try:
        cid = int(name)
    except ValueError:
        raise INVALID_CUSTOMER_ID from None

    try:
        customer = Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise NO_SUCH_CUSTOMER from None

    conditions = (
        lambda: ACCOUNT.root,
        lambda: ACCOUNT.admin and customer == ACCOUNT.customer)

    if any(condition() for condition in conditions):
        return customer

    if customer.id == CUSTOMER.id:
        return CUSTOMER

    raise NO_SUCH_CUSTOMER


def _settings() -> CustomerSettings:
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == CUSTOMER)
    except CustomerSettings.DoesNotExist:
        raise CUSTOMER_NOT_CONFIGURED from None


@authenticated
@root
def list_() -> JSON:
    """Lists available customers."""

    return JSON([customer.to_json(company=True) for customer in Customer])


@authenticated
def get(ident: int) -> JSON:
    """Allows services"""

    return JSON(get_customer(ident).to_json(company=True))


@authenticated
def get_logo() -> Binary:
    """Allows services"""

    return Binary(_settings().logo)


ROUTES = (
    ('GET', '/customer', list_),
    ('GET', '/customer/<ident>', get),
    ('GET', '/customer-logo', get_logo)
)
