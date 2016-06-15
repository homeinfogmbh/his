"""Core services"""

from itertools import chain
from importlib import import_module
from logging import INFO, getLogger, basicConfig

from homeinfo.lib.wsgi import InternalServerError, RequestHandler, WsgiApp


__all__ = ['HIS']


class HandlerNotAvailable(Exception):
    """Indicates that a given handler is not available"""

    pass


class HISMetaHandler(RequestHandler):
    """Generic HIS service template"""

    BASE_PACKAGE = 'his.mods'
    CLASS_NAME = 'Service'
    HANDLER_NA = InternalServerError('Handler not available.')

    def __init__(self, *args, **kwargs):
        """Sets a logger"""
        super().__init__(*args, **kwargs)
        self.logger = getLogger('HIS')

    def get(self):
        """Processes GET requests"""
        try:
            return self.handler(self.environ).get()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def post(self):
        """Processes POST requests"""
        try:
            return self.handler(self.environ).post()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def put(self):
        """Processes PUT requests"""
        try:
            return self.handler(self.environ).put()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    def delete(self):
        """Processes DELETE requests"""
        try:
            return self.handler(self.environ).delete()
        except HandlerNotAvailable:
            return self.HANDLER_NA

    @property
    def handler(self):
        """Returns the appropriate request handler"""
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


class HIS(WsgiApp):
    """HIS meta service"""

    REQUEST_HANDLER = HISMetaHandler
    DEBUG = True

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)
        basicConfig(level=INFO)

    def get_handler(self, environ):
        """Gets the appropriate service handler"""
