"""Request errors."""

from his.messages.api import HISMessage


__all__ = ['RequestError', 'MissingContentType']


class RequestError(HISMessage):
    """Indicates errors in the sent HTTP request."""

    STATUS = 400


class MissingContentType(RequestError):
    """Indicates a missing content type."""

    pass
