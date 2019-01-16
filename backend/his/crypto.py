"""HIS cryptography library."""

from random import choice
from string import ascii_letters, digits


__all__ = ['genpw']


POOL = ascii_letters + digits


def randchars(count, pool=POOL):
    """Yields random chars from the pool."""

    for _ in range(count):
        yield choice(pool)


def genpw(length=16, pool=POOL):
    """Generates a safe, radom password."""

    return ''.join(randchars(length, pool=pool))
