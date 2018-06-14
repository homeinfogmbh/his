"""Service related messages."""

from his.messages.api import Message

__all__ = [
    'NoServiceSpecified',
    'NoSuchService',
    'ServiceAdded',
    'ServiceAlreadyEnabled',
    'AmbiguousServiceTarget',
    'MissingServiceTarget']


class _ServiceMessage(Message):
    """Abstract common service message."""

    LOCALES = '/etc/his.d/locale/his/service.ini'


class NoServiceSpecified(_ServiceMessage):
    """Indicates that no service has been specified."""

    STATUS = 406


class NoSuchService(_ServiceMessage):
    """Indicates that the requested service does not exist."""

    STATUS = 404


class ServiceAdded(_ServiceMessage):
    """Indicates that the respective service has been added."""

    STATUS = 201


class ServiceAlreadyEnabled(_ServiceMessage):
    """Indicates that the respective service is already enabled."""

    STATUS = 409


class AmbiguousServiceTarget(_ServiceMessage):
    """Indicates that the respective target is ambiguous."""

    STATUS = 406


class MissingServiceTarget(_ServiceMessage):
    """Indicates that the respective target is missing."""

    STATUS = 406
