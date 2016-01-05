"""HIS cryptographic API"""

from ..config import his_config
from ..lib.crypto import PasswordManager

__all__ = ['load']


def load():
    """Loads the password manager"""
    iters = int(his_config.crypto['ITERS'])
    if iters > 0:
        with open(his_config.crypto['PEPPER'], 'r') as pepper_file:
            pepper = pepper_file.read()
        return PasswordManager(iters, pepper)
    else:
        raise ValueError('Hashing requires at least one iteration')
