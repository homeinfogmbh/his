"""HIS cryptography library."""

from random import choice
from string import ascii_letters, digits, punctuation

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

__all__ = [
    'MIN_LEN',
    'PasswordTooShortError',
    'hash_password',
    'verify_password',
    'genpw']


_PASSWORD_HASHER = PasswordHasher()
MIN_LEN = 8


class PasswordTooShortError(Exception):
    """Indicates that the provided password was too short."""

    def __init__(self, minlen, pwlen):
        """Sets minimum length and actual password length."""
        super().__init__(self, minlen, pwlen)
        self.minlen = minlen
        self.pwlen = pwlen

    def __str__(self):
        """Returns the respective error message."""
        return 'Password too short ({} / {} characters).'.format(
            self.pwlen, self.minlen)


def hash_password(passwd, minlen=MIN_LEN):
    """Creates a hash of the given password."""

    if len(passwd) < minlen:
        raise PasswordTooShortError(minlen, len(passwd))

    return _PASSWORD_HASHER.hash(passwd)


def verify_password(pwhash, passwd):
    """Verifies the respective password
    againts the given password hash.
    """

    try:
        return _PASSWORD_HASHER.verify(pwhash, passwd)
    except VerifyMismatchError:
        return False


def genpw(pool=ascii_letters+digits+punctuation, length=MIN_LEN):
    """Generates a password with the specified
    length from the character pool.
    """

    return ''.join(choice(pool) for _ in range(length))
