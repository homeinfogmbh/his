""" HIS password reset messages."""

from his.messages.api import HISMessage


__all__ = [
    'NO_TOKEN_SPECIFIED',
    'NO_PASSWORD_SPECIFIED',
    'PASSWORD_RESET_SENT',
    'PASSWORD_RESET_PENDING',
    'INVALID_RESET_TOKEN',
    'PASSWORD_SET']


NO_TOKEN_SPECIFIED = HISMessage('Missing password reset token.', status=400)
NO_PASSWORD_SPECIFIED = HISMessage('No password specified.', status=400)
PASSWORD_RESET_SENT = HISMessage(
    'An email with a password reset link has been sent.', status=200)
PASSWORD_RESET_PENDING = HISMessage(
    'A password reset is already pending.', status=423)
INVALID_RESET_TOKEN = HISMessage('Invalid password reset token.', status=401)
PASSWORD_SET = HISMessage('The new password has been set.', status=200)
