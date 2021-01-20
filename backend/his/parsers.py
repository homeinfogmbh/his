"""Type-like parser functions."""

from peewee import JOIN

from mdb import Address, Company, Customer

from his.orm.account import Account
from his.orm.service import Service


__all__ = ['account', 'service']


def account(string: str) -> Account:
    """Returns the account."""

    select = Account.select(Account, Customer, Company, Address).join(
        Customer).join(Company).join(Address, join_type=JOIN.LEFT_OUTER)

    try:
        ident = int(string)
    except ValueError:
        condition = False
    else:
        condition = Account.id == ident

    condition |= Account.name == string
    condition |= Account.email == string

    try:
        match, *excess = select.where(condition)
    except ValueError:
        raise ValueError('No such account.') from None

    if excess:
        raise ValueError('Ambiguous account selection.')

    return match


def service(string: str) -> Service:
    """Returns the respective service."""

    try:
        return Service.get(Service.name == string)
    except Service.DoesNotExist:
        raise ValueError('No such service.') from None
