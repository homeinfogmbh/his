"""HIS cryptographic library"""

import hmac
from uuid import uuid4
from hashlib import sha256

__all__ = ['hashpw', 'chkpw']


# XXX: Avoid to change!
_PEPPER = 'a852eca7-7a23-4b72-a48d-997047e18ef0'
_ITERS = 10000


def _hash_pw(passwd, salt):
    """Hashes a password"""
    psp = salt + _PEPPER + passwd
    return sha256(psp.encode()).hexdigest()


def hashpw(plaintext):
    """Hashes a password"""
    salt = hmac.new(str(uuid4()).encode()).hexdigest()
    hashed_pw = _hash_pw(plaintext, salt)
    for _ in range(0, _ITERS):
        hashed_pw = _hash_pw(hashed_pw, salt)
    return (hashed_pw, salt)


def chkpw(plaintext, pwhash, salt):
    """Verifies a plain text password"""
    hashed_pw = _hash_pw(plaintext, salt)
    for _ in range(0, _ITERS):
        hashed_pw = _hash_pw(hashed_pw, salt)
    return True if hashed_pw == pwhash else False
