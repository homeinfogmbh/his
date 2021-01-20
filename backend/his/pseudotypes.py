"""Type-like parser functions."""

from mdb import Address, Company, Customer

from peewee import JOIN

from his.orm import Account


__all__ = ['account']


def account(name: str) -> Account:
    """Parses an account."""

    select = Account.select(Account, Customer, Company, Address).join(
        Customer).join(Company).join(Address, join_type=JOIN.LEFT_OUTER)

    try:
        return select.where(Account.name == name).get()
    except Account.DoesNotExist:
        raise ValueError('No such account.') from None
