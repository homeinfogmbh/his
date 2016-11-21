"""Core services"""

from itertools import repeat
from time import sleep
from threading import Thread

from peewee import DoesNotExist

from homeinfo.lib.log import LoggingClass
from homeinfo.lib.wsgi import Error

from his.orm import Service, Session
from his.api.errors import NoSuchService

__all__ = ['HISProxy', 'SessionCleaner']


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
                    self.logger.info('Loaded handler: {}'.format(handler.name))
                    return handler


class SessionCleaner():
    """Periodically cleans up the sessions"""

    def __init__(self, interval=60):
        """Sets the cleanup interval"""
        self.interval = interval
        self._running = False
        self._thread = None

    def _run(self):
        """The actual cleanup loop"""
        while self._running:
            Session.cleanup()

            for _ in repeat(None, self.interval):
                if self._running:
                    sleep(1)
                else:
                    break

    def start(self):
        """Starts the cleanup thread"""
        if self._thread is None:
            self._running = True
            self._thread = Thread(target=self._run)
            self._thread.start()
            return True
        else:
            return False

    def stop(self):
        """Stops the cleanup thread"""
        self._running = False

        if self._thread is not None:
            self._thread.join()
            self._thread = None

        return True
