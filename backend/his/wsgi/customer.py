"""Customer-level meta services."""

from mdb import Customer
from wsgilib import JSON, Binary

from his.api import authenticated, root
from his.wsgi.functions import get_customer, get_customer_settings


__all__ = ['ROUTES']


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

    return Binary(get_customer_settings().logo)


ROUTES = (
    ('GET', '/customer', list_),
    ('GET', '/customer/<ident>', get),
    ('GET', '/customer-logo', get_logo)
)
