"""Meta-services for HIS"""

from peewee import DoesNotExist

from .db import Account, Session

__all__ = ['login', 'keepalive']


def login(name, passwd, duration=None):
    """Logs in a user"""
    try:
        account = Account.get(Account.name == name)
    except DoesNotExist:
        return False
    else:
        if Session.exists(account):
            return False
        else:
            try:
                duration = int(duration)
            except (ValueError, TypeError):
                duration = None
            return Session.open(account, duration=duration)


def keepalive(name, duration=None):
    """Keeps a session alive"""
    try:
        account = Account.get(Account.name == name)
    except DoesNotExist:
        return False
    else:
        try:
            session = Session.get(Session.account == account)
        except DoesNotExist:
            return False
        else:
            return session.renew(duration=duration)
