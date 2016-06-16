"""Meta-services for HIS"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import RequestHandler

__all__ = ['IncompleteImplementationError', 'HISService']


class IncompleteImplementationError(NotImplementedError):
    """Indicates an incomplete implementation of the service"""

    pass


class HISService(RequestHandler):
    """A generic HIS service"""

    PATH = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

    @classmethod
    def install(cls):
        """Installs the service into the registered database"""
        if cls.PATH is None or cls.NAME is None:
            raise IncompleteImplementationError()
        else:
            module = cls.__module__
            classname = cls.__name__

            try:
                service = Service.get(Service.path == cls.PATH)
            except DoesNotExist:
                service = Service()
                service.name = cls.NAME
                service.path = cls.PATH
                service.module = module
                service.handler = classname
                service.description = cls.DESCRIPTION
                service.promote = cls.PROMOTE
                return service.save()
            else:
                if service.name == self.name:
                    if service.module == self.module:
                        if service.handler == self.handler:
                            return True

                return False
