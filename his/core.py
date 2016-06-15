"""Core services"""

from itertools import chain

from homeinfo.lib.wsgi import InternalServerError, RequestHandler, WsgiApp


class HandlerNotAvailable(Exception):
    """Indicates that a given handler is not available"""

    pass


class HIS(WsgiApp):
    """HIS meta service"""

    def __init__(self):
        """Use library defaults, but always enable CORS"""
        super().__init__(cors=True)

    def get_handler(self, environ):
        """Gets the appropriate service handler"""


class HISHandler(RequestHandler):
    """Generic HIS service template"""

    BASE_PACKAGE = 'his.mods'
    CLASS_NAME = 'Service'

    def get(self):
        """Processes GET requests"""
        try:
            return self.handler.get()
        except HandlerNotAvailable:
            return InternalServerError('Handler not available.')

    def post(self):
        """Processes POST requests"""
        try:
            return self.handler.post()
        except HandlerNotAvailable:
            return InternalServerError('Handler not available.')

    def put(self):
        """Processes PUT requests"""
        try:
            return self.handler.put()
        except HandlerNotAvailable:
            return InternalServerError('Handler not available.')

    def delete(self):
        """Processes DELETE requests"""
        try:
            return self.handler.delete()
        except HandlerNotAvailable:
            return InternalServerError('Handler not available.')

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
