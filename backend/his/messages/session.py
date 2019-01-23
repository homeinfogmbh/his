"""Session related messages."""

from his.messages.facility import HIS_MESSAGE


__all__ = [
    'MISSING_CREDENTIALS',
    'INVALID_CREDENTIALS',
    'NO_SESSION_SPECIFIED',
    'NO_SUCH_SESSION',
    'SESSION_EXPIRED',
    'DURATION_OUT_OF_BOUNDS']


MISSING_CREDENTIALS = HIS_MESSAGE(
    'No user name and / or password specified.', status=401)
INVALID_CREDENTIALS = HIS_MESSAGE(
    'Invalid user name and / or password.', status=401)
NO_SESSION_SPECIFIED = HIS_MESSAGE('No session specified.', status=401)
NO_SUCH_SESSION = HIS_MESSAGE('Specified session does not exist.', status=404)
SESSION_EXPIRED = HIS_MESSAGE('Session expired.', status=401)
DURATION_OUT_OF_BOUNDS = HIS_MESSAGE(
    'Session duration is out of bounds.', status=400)
