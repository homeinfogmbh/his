"""HIS cryptographic library"""

import hmac
from uuid import uuid4
from hashlib import sha256
from itertools import repeat

from ..config import his_config

__all__ = ['Crypto']


class Crypto():
    """Crypto manager"""

    def __init__(self):
        """Sets the hashtype"""
        self.__pepper = hmac.new(
            his_config.crypto['PEPPER'].encode()).hexdigest()

    def _hash_pw(self, passwd, salt):
        """Hashes a password"""
        psp = passwd + salt + self.__pepper
        return sha256(psp.encode()).hexdigest()

    def _iter_hash(self, passwd, salt):
        """Hashes the password <self.iters> times"""
        hashed_pw = self._hash_pw(passwd, salt)
        for _ in repeat(None, self.iters):
            hashed_pw = self._hash_pw(hashed_pw, salt)
        return hashed_pw

    @property
    def iters(self):
        """Returns the pepper string"""
        return int(his_config.crypto['ITERS']) or 10000

    def hashpw(self, plaintext):
        """Hashes a password"""
        salt = hmac.new(str(uuid4()).encode()).hexdigest()
        hashed_pw = self._iter_hash(plaintext, salt)
        return (hashed_pw, salt)

    def chkpw(self, plaintext, pwhash, salt):
        """Verifies a plain text password"""
        hashed_pw = self._iter_hash(plaintext, salt)
        return True if hashed_pw == pwhash else False
