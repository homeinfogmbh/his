"""
Defines the HIS service databases
"""
from .config import db, wsgi
from .lib.error import UnsupportedAction
from peewee import MySQLDatabase
from os.path import join

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase', 'Service']


class HISServiceDatabase(MySQLDatabase):
    """A HIS service database"""
    def __init__(self, service, host=None, user=None,
                 passwd=None, threadlocals=False, **kwargs):
        if host is None:
            host = db.get('host')
        if user is None:
            user = db.get('user')
        if passwd is None:
            passwd = db.get('passwd')
        """Changes the name to create a '_'-separated namespace"""
        super().__init__('_'.join([db.get('master_db'), str(service)]),
                         host=host, user=user, passwd=passwd,
                         threadlocals=threadlocals, **kwargs)


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
        raise UnsupportedAction()

    def post(self, data, **kwargs):
        """Reaction POST request"""
        raise UnsupportedAction()

    def put(self, data, **kwargs):
        """Reaction PUT request"""
        raise UnsupportedAction()

    def delete(self, **kwargs):
        """Reaction DELETE request"""
        raise UnsupportedAction()


class Service(Resource):
    """Common service class"""
    def __init__(self):
        """Initializes relative to parent resource"""
        super().__init__(None)

    @property
    def resources(self):
        """Returns a generator of all the service's resources"""
        for attr in dir(self):
            if type(attr) is Resource:
                yield getattr(self, attr)
