"""HIS cryptographic library"""

import hmac
from uuid import uuid4
from hashlib import sha256
from itertools import repeat

from ..config import his_config

__all__ = ['PasswordManager']


class PasswordManager():
    """Generates and verifies passwords with salt and pepper"""

    def _hash_pw(self, passwd, salt):
        """Hashes a password"""
        psp = passwd + salt + self._pepper
        return sha256(psp.encode()).hexdigest()

    def _iter_hash(self, passwd, salt):
        """Hashes the password <self.iters> times"""
        hashed_pw = self._hash_pw(passwd, salt)
        for _ in repeat(None, self._iters):
            hashed_pw = self._hash_pw(hashed_pw, salt)
        return hashed_pw

    @property
    def _iters(self):
        """Returns the pepper string"""
        iters = int(his_config.crypto['ITERS'])
        if iters > 0:
            return iters
        else:
            raise ValueError('Hashing requires at least one iteration')

    @property
    def _pepper(self):
        """Returns the pepper string"""
        with open(his_config.crypto['PEPPER'], 'r') as pepper:
            return pepper.read()

    def hash(self, plaintext):
        """Hashes a password"""
        salt = hmac.new(str(uuid4()).encode()).hexdigest()
        hashed_pw = self._iter_hash(plaintext, salt)
        return (hashed_pw, salt)

    def verify(self, plaintext, pwhash, salt):
        """Verifies a plain text password"""
        hashed_pw = self._iter_hash(plaintext, salt)
        return True if hashed_pw == pwhash else False
