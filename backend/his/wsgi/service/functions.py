"""Common functions."""

from his.messages.service import NoSuchService
from his.orm import Service


__all__ = ['get_service']


def get_service(name):
    """Returns the respective service."""

    try:
        return Service.get(Service.name == name)
    except Service.DoesNotExist:
        raise NoSuchService()
