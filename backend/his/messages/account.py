"""Account related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NO_ACCOUNT_SPECIFIED',
    'NO_SUCH_ACCOUNT',
    'ACCOUNT_LOCKED',
    'ACCOUNT_CREATED',
    'ACCOUNT_DELETED',
    'ACCOUNT_PATCHED',
    'NOT_AUTHORIZED',
    'ACCOUNT_EXISTS',
    'ACCOUNTS_EXHAUSTED',
    'PASSWORD_TOO_SHORT']


NO_ACCOUNT_SPECIFIED = HISMessage('No account specified.', status=406)
NO_SUCH_ACCOUNT = HISMessage('No such account.', status=404)
ACCOUNT_LOCKED = HISMessage('Account is locked.', status=423)
ACCOUNT_CREATED = HISMessage('Account has been created.', status=201)
ACCOUNT_DELETED = HISMessage('Account has been deleted.', status=200)
ACCOUNT_PATCHED = HISMessage('Account has been patched.', status=200)
NOT_AUTHORIZED = HISMessage('Not authorized.', status=403)
ACCOUNT_EXISTS = HISMessage('Account already exists.', status=409)
ACCOUNTS_EXHAUSTED = HISMessage('Account quota is exhausted.', status=402)
PASSWORD_TOO_SHORT = HISMessage(
    'The specified password is too short.', status=415)
