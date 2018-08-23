"""Request group errors."""

from his.messages.api import HISMessage


__all__ = [
    'RequestGroupSizeOutOfBounds',
    'RequestGroupLimitExceeded',
    'NoSuchRequestGroup']


class RequestGroupSizeOutOfBounds(HISMessage):
    """Indicates that the requested request group size is
    larger than the maximum allowed request group size.
    """

    STATUS = 400


class RequestGroupLimitExceeded(HISMessage):
    """Indicates that the request group usage limit has been reached."""

    STATUS = 400


class NoSuchRequestGroup(HISMessage):
    """Indicates that the requested request group does not exist."""

    STATUS = 404
