"""Service related messages."""

from his.messages.api import HISMessage

__all__ = [
    'NoServiceSpecified',
    'NoSuchService',
    'ServiceAdded',
    'ServiceAlreadyEnabled',
    'AmbiguousServiceTarget',
    'MissingServiceTarget']


class NoServiceSpecified(HISMessage):
    """Indicates that no service has been specified."""

    STATUS = 406


class NoSuchService(HISMessage):
    """Indicates that the requested service does not exist."""

    STATUS = 404


class ServiceAdded(HISMessage):
    """Indicates that the respective service has been added."""

    STATUS = 201


class ServiceAlreadyEnabled(HISMessage):
    """Indicates that the respective service is already enabled."""

    STATUS = 409


class AmbiguousServiceTarget(HISMessage):
    """Indicates that the respective target is ambiguous."""

    STATUS = 406


class MissingServiceTarget(HISMessage):
    """Indicates that the respective target is missing."""

    STATUS = 406
