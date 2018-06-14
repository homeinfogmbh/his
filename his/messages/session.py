"""Session related messages."""

from his.messages.api import Message

__all__ = [
    'MissingCredentials',
    'InvalidCredentials',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'DurationOutOfBounds']


class _SessionMessage(Message):
    """Abstract common session message."""

    LOCALES = '/etc/his.d/locale/his/session.ini'


class MissingCredentials(_SessionMessage):
    """Indicates missing credentials."""

    STATUS = 401


class InvalidCredentials(_SessionMessage):
    """Indicates invalid credentials."""

    STATUS = 401


class NoSessionSpecified(_SessionMessage):
    """Indicates a missing session."""

    STATUS = 420


class NoSuchSession(_SessionMessage):
    """Indicates that the specified session does not exist."""

    STATUS = 404


class SessionExpired(_SessionMessage):
    """Indicates that the specified session has expired."""

    STATUS = 410


class DurationOutOfBounds(_SessionMessage):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal.
    """

    STATUS = 400
