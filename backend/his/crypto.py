"""HIS cryptography library."""

from getpass import getpass
from random import choices
from string import ascii_letters, digits
from sys import stderr


__all__ = ['genpw', 'read_passwd']


POOL = ascii_letters + digits


def genpw(length=16, pool=POOL):
    """Generates a safe, radom password."""

    return ''.join(choices(pool, k=length))


def read_passwd():
    """Reads a password."""

    while True:
        try:
            passwd = getpass('Password: ')
        except EOFError:
            continue

        try:
            repeat = getpass('Repeat password: ')
        except EOFError:
            continue

        if passwd and passwd == repeat:
            return passwd

        print('Passwords do not match.', file=stderr)
        continue
