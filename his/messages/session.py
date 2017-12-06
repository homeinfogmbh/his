"""Session related messages."""

from his.messages.common import Message

__all__ = [
    'MissingCredentials',
    'InvalidCredentials',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'DurationOutOfBounds']


class MissingCredentials(Message):
    """Indicates missing credentials."""

    STATUS = 401


class InvalidCredentials(Message):
    """Indicates invalid credentials."""

    STATUS = 401


class NoSessionSpecified(Message):
    """Indicates a missing session."""

    STATUS = 420


class NoSuchSession(Message):
    """Indicates that the specified session does not exist."""

    STATUS = 404


class SessionExpired(Message):
    """Indicates that the specified session has expired."""

    STATUS = 410


class DurationOutOfBounds(Message):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal.
    """

    STATUS = 400
