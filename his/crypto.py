"""HIS cryptography library"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

__all__ = [
    'PASSWORD_HASHER',
    'verify_password']


PASSWORD_HASHER = PasswordHasher()


def verify_password(pwhash, passwd):
    """Verifies the respective password
    againts the given password hash
    """

    try:
        return PASSWORD_HASHER.verify(pwhash, passwd)
    except VerifyMismatchError:
        return False
