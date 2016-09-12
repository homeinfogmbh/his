"""Core services"""

from logging import getLogger

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, WsgiApp

from his.orm import Service

__all__ = ['HIS']


logger = getLogger(__file__)


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class _ServiceProxy():

    def __getitem__(self, node):
        try:
            service = Service.get(Service.node == node)
        except DoesNotExist:
            raise KeyError()
        else:
            return service.handler


class HIS(WsgiApp):
    """HIS meta service"""

    DEBUG = True
    HANDLERS = _ServiceProxy()

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
