"""HIS cryptographic library"""

import hmac
from uuid import uuid4
from hashlib import sha256
from his.config import his_config

__all__ = ['Crypto']


class Crypto():
    """Crypto manager"""

    def __init__(self, cipher=None):
        """Sets the hashtype"""
        if cipher is None:
            self.cipher = sha256
        else:
            self.cipher = cipher

    def _hash_pw(self, passwd, salt):
        """Hashes a password"""
        psp = salt + self.pepper + passwd
        return self.cipher(psp.encode()).hexdigest()

    @property
    def pepper(self):
        """Returns the pepper string"""
        return hmac.new(his_config.crypto['PEPPER'].encode()).hexdigest()

    @property
    def iters(self):
        """Returns the pepper string"""
        return int(his_config.crypto['ITERS'])

    def hashpw(self, plaintext):
        """Hashes a password"""
        salt = hmac.new(str(uuid4()).encode()).hexdigest()
        hashed_pw = self._hash_pw(plaintext, salt)
        for _ in range(0, self.iters):
            hashed_pw = self._hash_pw(hashed_pw, salt)
        return (hashed_pw, salt)

    def chkpw(self, plaintext, pwhash, salt):
        """Verifies a plain text password"""
        hashed_pw = self._hash_pw(plaintext, salt)
        for _ in range(0, self.iters):
            hashed_pw = self._hash_pw(hashed_pw, salt)
        return True if hashed_pw == pwhash else False
