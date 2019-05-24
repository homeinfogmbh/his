"""HIS services."""

from wsgilib import JSON

from his.api import authenticated
from his.contextlocals import ACCOUNT
from his.orm import Service


__all__ = ['ROUTES']


@authenticated
def list_():
    """Lists promoted services."""

    if ACCOUNT.root:
        return JSON([service.to_json() for service in Service])

    return JSON([service.to_json() for service in Service.select().where(
        Service.promote == 1)])


ROUTES = (('GET', '/service', list_),)
