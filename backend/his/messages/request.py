"""Request errors."""

from his.messages.facility import HIS_MESSAGE


__all__ = ['INVALID_CONTENT_TYPE']


INVALID_CONTENT_TYPE = HIS_MESSAGE(
    'The provided content type could not be served.', status=406)
