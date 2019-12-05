"""Account related messages."""

from wsgilib import JSONMessage


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
    'PASSWORD_TOO_SHORT'
]


NO_ACCOUNT_SPECIFIED = JSONMessage('No account specified.', status=406)
NO_SUCH_ACCOUNT = JSONMessage('No such account.', status=404)
ACCOUNT_LOCKED = JSONMessage('Account is locked.', status=423)
ACCOUNT_CREATED = JSONMessage('Account has been created.', status=201)
ACCOUNT_DELETED = JSONMessage('Account has been deleted.', status=200)
ACCOUNT_PATCHED = JSONMessage('Account has been patched.', status=200)
NOT_AUTHORIZED = JSONMessage('Not authorized.', status=403)
ACCOUNT_EXISTS = JSONMessage('Account already exists.', status=409)
ACCOUNTS_EXHAUSTED = JSONMessage('Account quota is exhausted.', status=402)
PASSWORD_TOO_SHORT = JSONMessage(
    'The specified password is too short.', status=415)
