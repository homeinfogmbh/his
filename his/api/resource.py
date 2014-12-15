"""
Defines the HIS basic Resource template
"""
from ..config import wsgi
from ..lib.error import UnsupportedHTTPAction
from os.path import join

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase', 'Service']


class Resource():
    """
    A REST-capable resource
    """
    def __init__(self, parent):
        """Initializes relative to parent resource"""
        self.__parent = parent

    @property
    def parent(self):
        """Returns the parent resource"""
        return self.__parent

    @property
    def name(self):
        """Returns the resource's name"""
        return self.__class__.__name__

    @property
    def path(self):
        """Returns the resource's path"""
        return join(wsgi.get('root') if self.parent is None
                    else self.parent.path, self.name.lower())

    def get(self, **kwargs):
        """Reaction GET request"""
        raise UnsupportedHTTPAction()

    def post(self, data, **kwargs):
        """Reaction POST request"""
        raise UnsupportedHTTPAction()

    def put(self, data, **kwargs):
        """Reaction PUT request"""
        raise UnsupportedHTTPAction()

    def delete(self, **kwargs):
        """Reaction DELETE request"""
        raise UnsupportedHTTPAction()
