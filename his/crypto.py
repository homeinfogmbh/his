"""HIS cryptographic library"""

from hmac import new
from hashlib import sha256
from itertools import repeat
from string import printable
from random import choice

__all__ = ['PasswordGenerationError', 'load', 'PasswordManager']


class PasswordGenerationError(Exception):
    """Indicates an error during password generation"""

    pass


def load():
    """Loads the password manager"""
    try:
        iters = int(his_config.crypto['ITERS'])
    except (KeyError):
        raise ValueError('Missing iterations value in crypto config') from None
    except (ValueError, TypeError):
        raise ValueError('Invalid iterations value in crypto config') from None
    else:
        if iters > 0:
            try:
                pepper = his_config.crypto['PEPPER']
            except (KeyError):
                raise ValueError(
                    'Missing pepper value in crypto config') from None
            else:
                if pepper:
                    return PasswordManager(iters, pepper)
                else:
                    raise ValueError(
                        'Empty pepper value in crypto config') from None
        else:
            raise ValueError(
                'Hashing requires at least one iteration') from None


class PasswordManager():
    """Generates and verifies passwords with salt and pepper"""

    def __init__(self, iters, pepper):
        """Sets the hashing iterations and pepper value"""
        self._iters = iters
        self._pepper = pepper

    def _hash_pw(self, passwd, salt):
        """Hashes a password"""
        pw_salt = passwd + salt
        pw_salt_hmac = new(pw_salt.encode()).hexdigest()
        pw_salt_hmac_pepper = pw_salt_hmac + self._pepper
        pwhash = sha256(pw_salt_hmac_pepper.encode()).hexdigest()
        return pwhash

    def _iter_hash(self, passwd, salt):
        """Hashes the password self._iters times"""
        pwhash = self._hash_pw(passwd, salt)

        # Loop hashes, compensating for one already performed hash
        for _ in repeat(None, self._iters - 1):
            pwhash = self._hash_pw(pwhash, salt)

        return pwhash

    def hash(self, plaintext):
        """Hashes a password"""
        salt = self.random()
        pwhash = self._iter_hash(plaintext, salt)
        return (pwhash, salt)

    def verify(self, plaintext, pwhash, salt):
        """Verifies a plain text password"""
        hashed_pw = self._iter_hash(plaintext, salt)
        return hashed_pw == pwhash

    def random(self, length=16):
        """Generates a random password"""
        if length < 8:
            raise PasswordGenerationError(
                'Refusing to generate insecure '
                'password with less than 8 characters')
        else:
            password = ''

            for _ in repeat(None, length):
                password += choice(printable)

            pwlen = len(password)

            if pwlen == length:
                return password
            else:
                raise PasswordGenerationError(
                    'Expected password of length {desired_length} but got '
                    'password of length {actual_length}'.format(
                        desired_length=length, actual_length=pwlen))
