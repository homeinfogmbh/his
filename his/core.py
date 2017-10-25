"""Core services"""

from peewee import DoesNotExist

from fancylog import LoggingClass

from his.orm import Service
from his.api.messages import NoSuchService

__all__ = ['HISProxy']


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
                raise NoSuchService() from None
            else:
                self.logger.info('Proxying "{}"'.format(node))

                try:
                    handler = service.handler
                except ImportError:
                    self.logger.critical('No such module: {}'.format(
                        service.module))
                    raise NoSuchService() from None
                except AttributeError:
                    self.logger.critical('No such class: {}'.format(
                        service.class_))
                    raise NoSuchService() from None
                else:
                    self.logger.info('Loaded handler: {}'.format(handler))
                    return handler
