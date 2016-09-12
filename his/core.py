"""Core services"""

from peewee import DoesNotExist

from homeinfo.lib.log import Logger, LogLevel
from homeinfo.lib.rest import RestApp
from homeinfo.lib.wsgi import Error

from his.orm import Service
from his.config import config

__all__ = ['HIS']


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class _ServiceProxy():

    def __init__(self):
        """Sets the logger"""
        self.logger = Logger('ServiceProxy', level=LogLevel.SUCCESS)

    def __getitem__(self, node):
        """Returns the appropriate service for the node"""
        if node == config.wsgi['root']:
            self.logger.info('Proxying root')
            return self
        else:
            try:
                service = Service.get(Service.node == node)
            except DoesNotExist:
                self.logger.warning('No service for node "{}"'.format(node))
                raise KeyError()
            else:
                handler = service.handler
                self.logger.info('Proxying "{node}" to "{handler}"'.format(
                    node=node, handler=handler))
                return handler


class HIS(RestApp):
    """HIS meta service"""

    DEBUG = True
    HANDLERS = _ServiceProxy()

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
