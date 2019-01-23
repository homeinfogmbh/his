"""Request errors."""

from his.messages.api import HISMessage


__all__ = ['INVALID_CONTENT_TYPE']


INVALID_CONTENT_TYPE = HISMessage(
    'The provided content type could not be served.', status=406)
