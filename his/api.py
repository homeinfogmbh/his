"""Meta-services for HIS"""

from peewee import DoesNotExist

from .crypto import load
from .orm import Account, Session, AlreadyLoggedIn

from ..config import his_config

__all__ = ['login', 'keepalive']


class NoSuchAccount(Exception):
    """Indicates that no such account exists"""

    pass


class InvalidCredentials(Exception):
    """Indicates invalid user name / password combination"""

    pass


def login(name, passwd, duration=None):
    """Logs in a user"""
    try:
        account = Account.get(Account.name == name)
    except DoesNotExist:
        raise NoSuchAccount() from None
    else:
        if Session.exists(account):
            raise AlreadyLoggedIn()
        else:
            # Verify credentials
            pwmgr = load()
            if pwmgr.verify(passwd, account.pwhash, account.salt):
                return Session.open(account, duration=duration)
            else:
                raise InvalidCredentials() from None


def keepalive(name, duration=None):
    """Keeps a session alive"""
    try:
        account = Account.get(Account.name == name)
    except DoesNotExist:
        raise NoSuchAccount() from None
    else:
        try:
            session = Session.get(Session.account == account)
        except DoesNotExist:
            return False
        else:
            return session.renew(duration=duration)
