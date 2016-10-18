"""Meta-services for HIS"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.rest import ResourceHandler

from his.api.errors import NoSessionSpecified, NoSuchSession, SessionExpired, \
    ServiceNotRegistered, NotAuthorized
from his.core import HIS
from his.orm import Service, CustomerService, Account, Session

__all__ = [
    'IncompleteImplementationError',
    'HISService',
    'AuthenticatedService',
    'AuthorizedService']


class IncompleteImplementationError(NotImplementedError):
    """Indicates an incomplete implementation of the service"""

    pass


class HISService(ResourceHandler):
    """A generic HIS service"""

    NODE = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

    @classmethod
    def register(cls):
        """Registers a service in the core handler"""
        try:
            handler = HIS.HANDLERS[cls.NODE]
        except KeyError:
            HIS.HANDLERS[cls.NODE] = cls.NODE
            return True
        else:
            if handler is cls:
                return True
            else:
                return False

    @classmethod
    def install(cls):
        """Installs the service into the database index"""
        if cls.NODE is None or cls.NAME is None:
            raise IncompleteImplementationError() from None
        else:
            module = cls.__module__
            classname = cls.__name__

            try:
                service = Service.get(Service.node == cls.NODE)
            except DoesNotExist:
                service = Service()
                service.name = cls.NAME
                service.node = cls.NODE
                service.module = module
                service.handler = classname
                service.description = cls.DESCRIPTION
                service.promote = cls.PROMOTE
                return service.save()
            else:
                if service.name == cls.NAME:
                    if service.module == module:
                        if service.handler == classname:
                            return service

                return False


class AuthenticatedService(HISService):
    """A HIS service that is session-aware"""

    @property
    def session(self):
        """Returns the session or raises an error"""
        try:
            session_token = self.params['session']
        except KeyError:
            raise NoSessionSpecified() from None
        else:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                raise NoSuchSession() from None
            else:
                if session.alive:
                    return session
                else:
                    raise SessionExpired() from None

    @property
    def account(self):
        """Gets the verified targeted account"""
        account = self.session.account

        if account.root:
            try:
                return Account.find(self.params['account'])
            except (KeyError, DoesNotExist):
                return account
        elif account.admin:
            try:
                target_account = Account.find(self.params['account'])
            except (KeyError, DoesNotExist):
                return account
            else:
                if target_account.customer == account.customer:
                    return target_account
                else:
                    raise NotAuthorized() from None
        else:
            return account

    @property
    def customer(self):
        """Gets the verified targeted customer"""
        account = self.session.account

        if account.root:
            try:
                return Customer.find(self.params['customer'])
            except (KeyError, DoesNotExist):
                return account.customer
        else:
            return account.customer


class AuthorizedService(AuthenticatedService):
    """A HIS service that checks whether
    the account is enabled for it
    """

    @property
    def method(self):
        """Determines whether the account
        is allowed to use this service
        """
        try:
            node = self.__class__.NODE
        except AttributeError:
            raise IncompleteImplementationError() from None
        else:
            if not node:
                raise IncompleteImplementationError() from None
            else:
                try:
                    service = Service.get(Service.node == node)
                except DoesNotExist:
                    raise ServiceNotRegistered() from None
                else:
                    # Allow call iff
                    #   1) account is root or
                    #   2) account's customer is enabled for the service and
                    #       2a) account is admin or
                    #       2b) account is enabled for the service
                    #
                    account = self.session.account

                    if account.root:
                        return super().method
                    elif service in CustomerService.services(account.customer):
                        if account.admin:
                            return super().method
                        elif service in account.services:
                            return super().method
                        else:
                            raise NotAuthorized() from None
                    else:
                        raise NotAuthorized() from None
