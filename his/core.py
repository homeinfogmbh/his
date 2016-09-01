"""Core services"""

from importlib import import_module
from logging import getLogger
from os.path import relpath, normpath, commonprefix

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, InternalServerError, RequestHandler, \
    WsgiApp

from his.config import config
from his.orm import Service

__all__ = ['HIS']


logger = getLogger(__file__)


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class HISMeta(RequestHandler):
    """Generic HIS service template"""

    BASE_PACKAGE = 'his.mods'
    CLASS_NAME = 'Handler'

    def __call__(self):
        """Delegate to actual handler"""
        return self.handler()

    @property
    def root(self):
        """Returns the WSGI root path"""
        return normpath(config.wsgi['ROOT'])

    @property
    def relpath(self):
        """Returns the path info with the
        root prefix stripped from it
        """
        if commonprefix(self.path_info, self.root) == self.root:
            return relpath(self.path_info, self.root)
        else:
            raise InternalServerError(
                'Path "{path}" not in root "{root}"'.format(
                    path=self.path_info, root=self.root))

    @property
    def handler(self):
        """Returns the appropriate request handler class"""
        try:
            service = Service.by_relpath(self.relpath)
        except DoesNotExist:
            raise Error('No handler for path: "{}"'.format(self.relpath))

        module_path = service.module
        class_name = service.handler

        try:
            module = import_module(module_path)
            handler = getattr(module, class_name)
        except ImportError:
            msg = 'Module "{}" is not installed.'.format(module_path)
            logger.critical(msg)
            raise Error(msg)
        except AttributeError:
            msg = 'Module "{module}" has no handler "{handler}".'.format(
                module=module_path, handler=class_name)
            logger.critical(msg)
            raise Error(msg)
        else:
            return handler(
                self.environ,
                self.cors,
                self.date_format,
                self.debug)

    def get(self):
        """Processes GET requests"""
        return self.handler.get()

    def post(self):
        """Processes POST requests"""
        return self.handler.post()

    def put(self):
        """Processes PUT requests"""
        return self.handler.put()

    def delete(self):
        """Processes DELETE requests"""
        return self.handler.delete()


class HIS(WsgiApp):
    """HIS meta service"""

    REQUEST_HANDLER = HISMeta
    DEBUG = True

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
