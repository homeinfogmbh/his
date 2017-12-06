"""Service related messages."""

from his.messages.common import Message

__all__ = [
    'NoServiceSpecified',
    'NoSuchService',
    'ServiceAdded',
    'ServiceAlreadyEnabled',
    'AmbiguousServiceTarget',
    'MissingServiceTarget']


class NoServiceSpecified(Message):
    """Indicates that no service has been specified."""

    STATUS = 406


class NoSuchService(Message):
    """Indicates that the requested service does not exist."""

    STATUS = 404


class ServiceAdded(Message):
    """Indicates that the respective service has been added."""

    STATUS = 201


class ServiceAlreadyEnabled(Message):
    """Indicates that the respective service is already enabled."""

    STATUS = 409


class AmbiguousServiceTarget(Message):
    """Indicates that the respective target is ambiguous."""

    STATUS = 406


class MissingServiceTarget(Message):
    """Indicates that the respective target is missing."""

    STATUS = 406
