"""Customer-level meta services."""

from typing import Optional

from peewee import ModelSelect

from mdb import Company, Customer
from wsgilib import JSON, Binary

from his.api import authenticated, root
from his.wsgi.functions import get_customer, get_customer_settings


__all__ = ['ROUTES']


def get_customers() -> ModelSelect:
    """Selects all customers."""

    return Customer.select(Customer, Company).join(Company).where(True)


@authenticated
@root
def list_() -> JSON:
    """Lists available customers."""

    return JSON([record.to_json(company=True) for record in get_customers()])


@authenticated
def get(ident: Optional[int] = None) -> JSON:
    """Allows services"""

    return JSON(get_customer(ident).to_json(company=True))


@authenticated
def get_logo() -> Binary:
    """Allows services"""

    return Binary(get_customer_settings().logo)


ROUTES = (
    ('GET', '/customer', list_),
    ('GET', '/customer/<int:ident>', get),
    ('GET', '/customer/!', lambda: get()),  # pylint: disable=W0108
    ('GET', '/customer-logo', get_logo)
)
