"""Core services"""

from logging import getLogger

from peewee import DoesNotExist

from homeinfo.lib.log import Logger
from homeinfo.lib.rest import RestApp
from homeinfo.lib.wsgi import Error

from his.orm import Service

__all__ = ['HIS']


logger = getLogger(__file__)


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class _ServiceProxy():

    def __init__(self):
        """Sets the logger"""
        self.logger = Logger('ServiceProxy')

    def __getitem__(self, node):
        """Returns the appropriate service for the node"""
        try:
            service = Service.get(Service.node == node)
        except DoesNotExist:
            self.logger.warning('No service for node "{}"'.format(node))
            raise KeyError()
        else:
            return service.handler


class HIS(RestApp):
    """HIS meta service"""

    DEBUG = True
    HANDLERS = _ServiceProxy()

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
