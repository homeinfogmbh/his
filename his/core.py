"""Core services"""

from peewee import DoesNotExist

from homeinfo.lib.log import LoggingClass
from homeinfo.lib.wsgi import Error

from his.orm import Service

__all__ = ['HISProxy']


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class HISProxy(LoggingClass):
    """Proxies handler requests"""

    def __init__(self, root):
        """Sets the logger"""
        super().__init__()
        self.root = root

    def __getitem__(self, node):
        """Returns the appropriate service for the node"""
        if node == self.root:
            self.logger.info('Proxying root: {}'.format(self.root))
            return self
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
