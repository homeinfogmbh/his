"""Request errors."""

from his.messages.api import HISMessage


__all__ = ['RequestError', 'InvalidContentType']


class RequestError(HISMessage):
    """Indicates errors in the sent HTTP request."""

    STATUS = 400


class InvalidContentType(RequestError):
    """Indicates an invalid content type."""

    STATUS = 406
