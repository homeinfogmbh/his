"""Request management."""

from contextlib import suppress
from datetime import datetime, timedelta
from uuid import uuid4

from his.messages.request import RequestGroupSizeOutOfBounds, \
    RequestGroupLimitExceeded, NoSuchRequestGroup


__all__ = ['REQUEST_GROUPS']


MAX_SIZE = 256


class _RequestGroup:
    """A group of requests."""

    __slots__ = ('_session', 'size', 'id', 'uses', 'start')

    def __init__(self, session, size):
        """Sets the amount of requests in this group."""
        if size > MAX_SIZE:
            raise RequestGroupSizeOutOfBounds(size=size, max=MAX_SIZE)

        self._session = session
        self.size = size
        self.uses = 0
        self.start = datetime.now()

    @property
    def expired(self):
        """Determines whether the request group is expired."""
        return datetime.now() - self.start > timedelta(minutes=1)

    @property
    def valid(self):
        """Determines whether the request is valid."""
        return self.uses < self.size and not self.expired

    @property
    def session(self):
        """Returns a cached session."""
        if self.valid:
            self.uses += 1
            return self._session

        raise RequestGroupLimitExceeded()


class _RequestGroupCache(dict):
    """Caches request groups."""

    def add(self, session, size):
        """Adds a request group with the respective size."""
        self[uuid4()] = _RequestGroup(session, size)

    def get_session(self, request_group_token):
        """Returns the respective request group iff it is valid."""
        try:
            request_group = self[request_group_token]
        except KeyError:
            raise NoSuchRequestGroup()

        with suppress(RuntimeError):    # Dict might change during request.
            self.cleanup()

        if request_group.valid:
            return request_group.session

        self.pop(request_group_token)
        raise RequestGroupLimitExceeded()

    def cleanup(self):
        """Cleans up invalid request groups."""
        invalid_keys = set()

        for key, request_group in self.items():
            if not request_group.valid:
                invalid_keys.add(key)

        for key in invalid_keys:
            self.pop(key)


REQUEST_GROUPS = _RequestGroupCache()
