"""Core services"""

from itertools import chain
from importlib import import_module
from logging import INFO, getLogger, basicConfig
from os.path import relpath

from homeinfo.lib.wsgi import InternalServerError, RequestHandler, WsgiApp

from his.config import config

__all__ = ['HIS']


class HandlerNotAvailable(Exception):
    """Indicates that a given handler is not available"""

    pass


class HISMetaHandler(RequestHandler):
    """Generic HIS service template"""

    BASE_PACKAGE = 'his.mods'
    CLASS_NAME = 'Handler'
    HANDLER_NA = InternalServerError('Handler not available.')

    def __init__(self, environ, *args, **kwargs):
        """Sets a logger"""
        basicConfig(level=INFO)
        self.logger = getLogger('HIS')

        if environ['PATH_INFO'].startswith(self.root):
            environ['PATH_INFO'] = relpath(environ['PATH_INFO'], self.root)
        else:
            raise InternalServerError(
                'Path "{path}" not in root "{root}"'.format(
                    path=environ['PATH_INFO'], root=self.root))

        super().__init__(environ, *args, **kwargs)

    def get(self):
        """Processes GET requests"""
        try:
            return self.handler.get()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def post(self):
        """Processes POST requests"""
        try:
            return self.handler.post()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def put(self):
        """Processes PUT requests"""
        try:
            return self.handler.put()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def delete(self):
        """Processes DELETE requests"""
        try:
            return self.handler.delete()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    @property
    def root(self):
        """Returns the WSGI root path"""
        return config.wsgi['ROOT']

    @property
    def handler_class(self):
        """Returns the appropriate request handler class"""
        try:
            module_path = '.'.join(chain([self.BASE_PACKAGE], self.path))
            module = import_module(module_path)
            return getattr(module, self.CLASS_NAME)
        except ImportError:
            self.logger.critical(
                'Could not import module from path: {path}'.format(
                    path=module_path))
            raise HandlerNotAvailable()
        except AttributeError:
            self.logger.critical(
                'Could not get attribute {cls} from module {module}'.format(
                    cls=self.CLASS_NAME, module=module))
            raise HandlerNotAvailable()

    @property
    def next_handler(self):
        """Returns the next handler's name"""
        return self.path[-1]

    @property
    def handler(self):
        """Returns the appropriate request handler's instance"""
        return self.handler_class(self.next_handler, self.environ)


class HIS(WsgiApp):
    """HIS meta service"""

    REQUEST_HANDLER = HISMetaHandler
    DEBUG = True

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
