"""HIS cryptography library"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

__all__ = ['hash_password', 'verify_password']


_PASSWORD_HASHER = PasswordHasher()


def hash_password(passwd):
    """Creates a hash of the given password."""

    return _PASSWORD_HASHER.hash(passwd)


def verify_password(pwhash, passwd):
    """Verifies the respective password
    againts the given password hash
    """

    try:
        return _PASSWORD_HASHER.verify(pwhash, passwd)
    except VerifyMismatchError:
        return False
