"""Type-like parser functions."""

from his.orm import Account


__all__ = ['account']


def account(name: str) -> Account:
    """Parses an account."""

    try:
        return Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise ValueError('No such account.') from None
