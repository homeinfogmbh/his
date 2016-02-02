"""HIS WSGI controller"""

from os.path import relpath

from homeinfo.lib.wsgi import InternalServerError, WsgiApp


class NotAModule(Exception):
    """Indicates that the called path is not of a module"""

    pass


class HISController(WsgiApp):
    """Main HIS controller"""

    def __init__(self, root):
        super().__init__()
        self.root = root

    def path(self, path_info):
        """Gets a module from a path"""
        return super().path(relpath(path_info, self.root))

    def submodule(self, path):
        """Gets the submodule from the path"""
        if len(path) >= 2:
            if path[0] == 'module':
                return (path[1], '/'.join(path[2:]))
            else:
                raise NotAModule()
        else:
            raise NotAModule()

    def run(self, environ):
        """Wraps the run() mehtod to differ
        between core API calls and module calls
        """
        path = self.path(self.path_info(environ))
        qd = self.qd(self.query_string(environ))
        submodule = self._submodule(path)
        try:
            module_name, module_path = self.submodule(path)
        except NotAModule:
            return super().run(environ)
        else:
            try:
                module = self.load_module(module_name)
            except NoSuchModule:
                return InternalServerError(
                    'No such module: {0}'.format(module_name))
            else:
                # Update PATH_INFO for sub module
                environ['PATH_INFO'] = module_path
                return module.run(environ)
