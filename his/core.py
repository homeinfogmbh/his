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
    CLASS_NAME = 'Handler'
    HANDLER_NA = InternalServerError('Handler not available.')

    def __init__(self, root, *args, **kwargs):
        """Sets a logger"""
        self.logger = getLogger('HIS')
        super().__init__(*args, **kwargs)
        self.root = root

    @property
    def rela_path(self):
        """Returns the path nodes relative to the root"""
        rela_path = self.path

        for node in self.root:
            # XXX: This may throw an IndexError
            if rela_path[0] == node:
                rela_path = rela_path[1:]
            else:
                raise ValueError(
                    'Unexpected path node: {actual_node}. '
                    'Expected {desired_node}'.format(
                        actual_node=rela_path[0], desired_node=node))

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
    def handler(self):
        """Returns the appropriate request handler's instance"""
        return self.handler_class(
            self.environ,
            self.cors,
            self.date_format,
            self.debug)


class HIS(WsgiApp):
    """HIS meta service"""

    REQUEST_HANDLER = HISMetaHandler
    DEBUG = True

    def __init__(self, root=None):
        """Use library defaults, but always enable CORS"""
        basicConfig(level=INFO)
        super().__init__(cors=True)

        if root is None:
            self.root = []
        else:
            self.root = [node for node in root.split('/') if node]

        self.REQUEST_HANDLER.ROOT = self.root

    def handler(self, environ):
        """Returns the handler instance"""
        return self.REQUEST_HANDLER(
            environ, self.root, self.cors, self.date_format, self.debug)
