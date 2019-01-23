"""Session related messages."""

from his.messages.api import HISMessage


__all__ = [
    'MISSING_CREDENTIALS',
    'INVALID_CREDENTIALS',
    'NO_SESSION_SPECIFIED',
    'NO_SUCH_SESSION',
    'SESSION_EXPIRED',
    'DURATION_OUT_OF_BOUNDS']


MISSING_CREDENTIALS = HISMessage(
    'No user name and / or password specified.', status=401)
INVALID_CREDENTIALS = HISMessage(
    'Invalid user name and / or password.', status=401)
NO_SESSION_SPECIFIED = HISMessage('No session specified.', status=401)
NO_SUCH_SESSION = HISMessage('Specified session does not exist.', status=404)
SESSION_EXPIRED = HISMessage('Session expired.', status=401)
DURATION_OUT_OF_BOUNDS = HISMessage(
    'Session duration is out of bounds.', status=400)
