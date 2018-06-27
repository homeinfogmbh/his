"""HIS cryptography library."""

from random import choice
from string import ascii_letters, digits, punctuation

__all__ = ['genpw']


def genpw(pool=ascii_letters+digits+punctuation, length=8):
    """Generates a password with the specified
    length from the character pool.
    """

    return ''.join(choice(pool) for _ in range(length))
