"""
Handles the request_uri from the environ dictionary
"""
from string import printable

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['ResourceHandler']


class ResourceHandler():
    """
    Handles queries
    """
    __PATH_SEP = '/'

    def __init__(self, path):
        """Initializes with a request URI to process"""
        self.__path = path

    @property
    def PATH_SEP(self):
        """Returns the path separator"""
        return self.__PATH_SEP

    @property
    def path(self):
        """Returns the request path"""
        return self.__path

    @property
    def resource(self):
        """Returns a list of resource path nodes"""
        return self.path.split(self.PATH_SEP)
