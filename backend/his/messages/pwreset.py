""" HIS password reset messages."""

from his.messages.facility import HIS_MESSAGE


__all__ = [
    'NO_TOKEN_SPECIFIED',
    'NO_PASSWORD_SPECIFIED',
    'PASSWORD_RESET_SENT',
    'PASSWORD_RESET_PENDING',
    'INVALID_RESET_TOKEN',
    'PASSWORD_SET']


NO_TOKEN_SPECIFIED = HIS_MESSAGE('Missing password reset token.', status=400)
NO_PASSWORD_SPECIFIED = HIS_MESSAGE('No password specified.', status=400)
PASSWORD_RESET_SENT = HIS_MESSAGE(
    'An email with a password reset link has been sent.', status=200)
PASSWORD_RESET_PENDING = HIS_MESSAGE(
    'A password reset is already pending.', status=423)
INVALID_RESET_TOKEN = HIS_MESSAGE('Invalid password reset token.', status=401)
PASSWORD_SET = HIS_MESSAGE('The new password has been set.', status=200)
