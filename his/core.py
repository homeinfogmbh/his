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


class RootProxy():
    """Proxies root queries"""

    def __init__(self, root):
        """Sets the logger"""
        self.root = root
        self.logger = Logger(self.__class__.__name__, level=LogLevel.SUCCESS)

    def __getitem__(self, node):
        """Returns the appropriate service for the node"""
        if node == config.wsgi['root']:
            self.logger.info('Proxying root')
            return self.root
        else:
            try:
                service = Service.get(Service.node == node)
            except DoesNotExist:
                self.logger.warning('No service for node "{}"'.format(node))
                raise KeyError()
            else:
                self.logger.info('Proxying "{}"'.format(node))
                handler = service.handler
                self.logger.info('Loading handler "{}"'.format(handler))
                return handler


class HIS(RestApp):
    """HIS meta service"""

    DEBUG = True

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
        self.HANDLERS = RootProxy(self)
