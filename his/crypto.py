"""HIS cryptography library."""

from random import choice
from string import ascii_letters, digits, punctuation

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

__all__ = ['PasswordTooShort', 'hash_password', 'verify_password']


_PASSWORD_HASHER = PasswordHasher()


class PasswordTooShort(ValueError):
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


def hash_password(passwd, minlen=8):
    """Creates a hash of the given password."""

    if len(passwd) < minlen:
        raise PasswordTooShort(minlen, len(passwd))

    return _PASSWORD_HASHER.hash(passwd)


def verify_password(pwhash, passwd):
    """Verifies the respective password
    againts the given password hash.
    """

    try:
        return _PASSWORD_HASHER.verify(pwhash, passwd)
    except VerifyMismatchError:
        return False


def genpw(pool=ascii_letters+digits+punctuation, length=8):
    """Generates a password with the specified
    length from the character pool.
    """

    return ''.join(choice(pool) for _ in range(length))
