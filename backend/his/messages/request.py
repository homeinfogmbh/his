"""Request errors."""

from wsgilib import JSONMessage


__all__ = ['INVALID_CONTENT_TYPE']


INVALID_CONTENT_TYPE = JSONMessage(
    'The provided content type could not be served.', status=406)
