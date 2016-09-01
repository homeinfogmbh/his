"""Meta-services for HIS"""

from os.path import relpath

from peewee import DoesNotExist

from homeinfo.lib.wsgi import RequestHandler

from his.orm import Service, CustomerService, Session
from his.api.errors import NoSessionSpecified, NoSuchSession, SessionExpired, \
    ServiceNotRegistered, NotAuthorized
from his.core import HISRequestHandler

__all__ = [
    'IncompleteImplementationError',
    'HISService',
    'AuthenticatedService',
    'AccountService',
    'AuthorizedService']


class IncompleteImplementationError(NotImplementedError):
    """Indicates an incomplete implementation of the service"""

    pass


class HISService(HISRequestHandler):
    """A generic HIS service"""

    PATH = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

    @property
    def resource(self):
        """Returns the resource path"""
        return relpath(self.relpath, self.PATH)

    @classmethod
    def install(cls):
        """Installs the service into
        the registered database
        """
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
                if service.name == cls.NAME:
                    if service.module == module:
                        if service.handler == classname:
                            return True

                return False


class AuthenticatedService(HISService):
    """A HIS service that is session-aware"""

    @property
    def session(self):
        """Returns the session or raises an error"""
        try:
            session_token = self.query_dict['session']
        except KeyError:
            raise NoSessionSpecified()
        else:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                raise NoSuchSession()
            else:
                if session.active:
                    return session
                else:
                    raise SessionExpired()


class AccountService(AuthenticatedService):
    """A HIS service that is account- and customer-aware"""

    @property
    def account(self):
        """Returns the respective account"""
        return self.session.account

    @property
    def customer(self):
        """Returns the respective customer"""
        return self.session.account.customer


class AuthorizedService(AccountService):
    """A HIS service that checks whether
    the account is enabled for it
    """

    def __call__(self):
        """Determines whether the account
        is allowed to use this service
        """
        try:
            path = self.__class__.PATH
        except AttributeError:
            raise IncompleteImplementationError()
        else:
            if not path:
                raise IncompleteImplementationError()
            else:
                try:
                    service = Service.get(Service.path == path)
                except DoesNotExist:
                    raise ServiceNotRegistered()
                else:
                    # Allow call iff
                    #   1) account is root or
                    #   2) account's customer is enabled for the service and
                    #       2a) account is admin or
                    #       2b) account is enabled for the service
                    #
                    if self.account.root:
                        return super().__call__()
                    elif service in CustomerService.services(self.customer):
                        if self.account.admin:
                            return super().__call__()
                        elif service in self.account.services:
                            return super().__call__()
                        else:
                            raise NotAuthorized()
                    else:
                        raise NotAuthorized()
