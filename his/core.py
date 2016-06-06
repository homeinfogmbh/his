"""Core services"""

from itertools import chain

from homeinfo.lib.wsgi import WsgiApp


def get_service(path_info):
    """Tries to get a service handler by the provided path info"""

    module_base = 'his.mods'
    class_name = 'Service'
    nodes = path_info.split('/')
    module_path = '.'.join(chain([module_base], nodes))
    module = import_module(module_path)
    return getattr(module, class_name)


class HIS(WsgiApp):
    """HIS meta service"""

    def get(self, environ):
        path_info = self.path_info(environ)

        try:
            service = get_service(path_info)
        except ImportError:
            self.logger.critical('Could not import module path: {}'.format(
                path_info))
        except AttributeError:
            pass  # TODO
