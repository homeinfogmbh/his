"""Request group handling."""

from wsgilib import JSON

from his.api import authenticated
from his.request import REQUEST_GROUPS
from his.globals import SESSION


__all__ = ['ROUTES']


@authenticated
def post(size):
    """Creates a new request group."""

    return JSON(REQUEST_GROUPS.add(SESSION, size))


ROUTES = (('POST', '/requestgroup/<int:size>', post, 'add_request_group'),)
