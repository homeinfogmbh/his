"""Session related messages."""

from his.messages.api import HISMessage

__all__ = [
    'MissingCredentials',
    'InvalidCredentials',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'DurationOutOfBounds']


class MissingCredentials(HISMessage):
    """Indicates missing credentials."""

    STATUS = 401


class InvalidCredentials(HISMessage):
    """Indicates invalid credentials."""

    STATUS = 401


class NoSessionSpecified(HISMessage):
    """Indicates a missing session."""

    STATUS = 420


class NoSuchSession(HISMessage):
    """Indicates that the specified session does not exist."""

    STATUS = 404


class SessionExpired(HISMessage):
    """Indicates that the specified session has expired."""

    STATUS = 410


class DurationOutOfBounds(HISMessage):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal.
    """

    STATUS = 400
