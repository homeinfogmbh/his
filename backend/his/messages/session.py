"""Session related messages."""

from wsgilib import JSONMessage


__all__ = [
    'MISSING_CREDENTIALS',
    'INVALID_CREDENTIALS',
    'NO_SESSION_SPECIFIED',
    'NO_SUCH_SESSION',
    'SESSION_EXPIRED',
    'DURATION_OUT_OF_BOUNDS']


MISSING_CREDENTIALS = JSONMessage(
    'No user name and / or password specified.', status=401)
INVALID_CREDENTIALS = JSONMessage(
    'Invalid user name and / or password.', status=401)
NO_SESSION_SPECIFIED = JSONMessage('No session specified.', status=401)
NO_SUCH_SESSION = JSONMessage('Specified session does not exist.', status=404)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
DURATION_OUT_OF_BOUNDS = JSONMessage(
    'Session duration is out of bounds.', status=400)
