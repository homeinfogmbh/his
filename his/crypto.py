"""HIS cryptography library"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

__all__ = [
    'passwd_hasher',
    'verify_password']


passwd_hasher = PasswordHasher()


def verify_password(pwhash, passwd):
    """Verifies the respective password
    againts the given password hash
    """

    try:
        return passwd_hasher.verify(pwhash, passwd)
    except VerifyMismatchError:
        return False
