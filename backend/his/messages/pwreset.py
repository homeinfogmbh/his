""" HIS password reset messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_TOKEN_SPECIFIED',
    'NO_PASSWORD_SPECIFIED',
    'PASSWORD_RESET_SENT',
    'PASSWORD_RESET_PENDING',
    'INVALID_RESET_TOKEN',
    'PASSWORD_SET'
]


NO_TOKEN_SPECIFIED = JSONMessage('Missing password reset token.', status=400)
NO_PASSWORD_SPECIFIED = JSONMessage('No password specified.', status=400)
PASSWORD_RESET_SENT = JSONMessage(
    'An email with a password reset link has been sent.', status=200)
PASSWORD_RESET_PENDING = JSONMessage(
    'A password reset is already pending.', status=423)
INVALID_RESET_TOKEN = JSONMessage('Invalid password reset token.', status=401)
PASSWORD_SET = JSONMessage('The new password has been set.', status=200)
