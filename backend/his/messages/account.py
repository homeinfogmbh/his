"""Account related messages."""

from his.messages.facility import HIS_MESSAGE


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


NO_ACCOUNT_SPECIFIED = HIS_MESSAGE('No account specified.', status=406)
NO_SUCH_ACCOUNT = HIS_MESSAGE('No such account.', status=404)
ACCOUNT_LOCKED = HIS_MESSAGE('Account is locked.', status=423)
ACCOUNT_CREATED = HIS_MESSAGE('Account has been created.', status=201)
ACCOUNT_DELETED = HIS_MESSAGE('Account has been deleted.', status=200)
ACCOUNT_PATCHED = HIS_MESSAGE('Account has been patched.', status=200)
NOT_AUTHORIZED = HIS_MESSAGE('Not authorized.', status=403)
ACCOUNT_EXISTS = HIS_MESSAGE('Account already exists.', status=409)
ACCOUNTS_EXHAUSTED = HIS_MESSAGE('Account quota is exhausted.', status=402)
PASSWORD_TOO_SHORT = HIS_MESSAGE(
    'The specified password is too short.', status=415)
