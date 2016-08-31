"""Core services"""

from importlib import import_module
from logging import INFO, getLogger, basicConfig
from os.path import relpath

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, InternalServerError, RequestHandler, \
    WsgiApp

from his.config import config
from his.orm import Service

__all__ = ['HIS']


class HandlerNotAvailable(Error):
    """Indicates that a given handler is not available"""

    def __init__(self):
        super().__init__('No handler available')


class HISMetaHandler(RequestHandler):
    """Generic HIS service template"""

    BASE_PACKAGE = 'his.mods'
    CLASS_NAME = 'Handler'

    def __init__(self, environ, cors, date_format, debug):
        """Sets a logger"""
        basicConfig(level=INFO)
        self.logger = getLogger('HIS')
        super().__init__(environ, cors, date_format, debug)

    def __call__(self):
        """Delegate to actual handler"""
        return self.handler()

    @property
    def root(self):
        """Returns the WSGI root path"""
        return config.wsgi['ROOT']

    @property
    def path_info(self):
        """Returns the path info with the
        root prefix stripped from it
        """
        if super().path_info.startswith(self.root):
            return relpath(path_info, self.root)
        else:
            raise InternalServerError(
                'Path "{path}" not in root "{root}"'.format(
                    path=super().path_info, root=self.root))

    @property
    def module_path(self):
        """Returns the module path"""
        if self.request_method == 'PUT':
            # On PUT the last node is resource identifier.
            return self.path_info[:-1]
        else:
            return self.path_info

    @property
    def resource(self):
        """Returns the respective resource identifier"""
        if self.request_method == 'PUT':
            # Last node is resource identifier
            return self.path_info[-1]

    @property
    def handler(self):
        """Returns the appropriate request handler class"""
        try:
            service = Service.get(Service.path == self.module_path)
        except DoesNotExist:
            raise Error('No handler registered for path: {path}'.format(
                path=self.path_info))
        else:
            module_path = service.module
            class_name = service.handler

            try:
                module = import_module(module_path)
                handler = getattr(module, class_name)
            except ImportError:
                msg = 'Module "{}" is not installed.'.format(module_path)
                self.logger.critical(msg)
                raise Error(msg)
            except AttributeError:
                msg = 'Module "{module}" has no handler "{handler}".'.format(
                    module=module_path, handler=class_name)
                self.logger.critical(msg)
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

    REQUEST_HANDLER = HISMetaHandler
    DEBUG = True

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
