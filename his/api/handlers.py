"""Meta-services for HIS"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from wsgilib import InternalServerError, ResourceHandler

from his.api.messages import IncompleteImplementationError, \
    NoSessionSpecified, NoSuchSession, SessionExpired, ServiceNotRegistered, \
    NotAuthorized, NoSuchCustomer, NoSuchAccount
from his.orm import Service, CustomerService, Account, Session

__all__ = [
    'HISService',
    'AuthenticatedService',
    'AuthorizedService',
    'AdminService',
    'RootService']


class CheckPassed(Exception):
    """Indicates that a service check passed"""

    pass


class HISService(ResourceHandler):
    """A generic HIS service"""

    NODE = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

    def __call__(self):
        """Check service and run it.

        Succeeded cheks are determined by a certain exception, so that faulty
        implementations of SomeService._check() or accidental overrides of
        those will most likely result in a failed service check as they do
        not throw this special exception.
        """
        try:
            self._check()
        except CheckPassed:
            return super().__call__()
        else:
            raise InternalServerError('Service check failed.') from None

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

    def _check(self):
        raise CheckPassed()


class AuthenticatedService(HISService):
    """A HIS service that is session-aware"""

    def _check(self):
        """Checks whether the account is logged in"""
        if self.session.alive:
            raise CheckPassed() from None
        else:
            raise SessionExpired() from None

    @property
    def session(self):
        """Returns the session or raises an error"""
        try:
            session_token = self.query['session']
        except KeyError:
            raise NoSessionSpecified() from None
        else:
            try:
                return Session.get(Session.token == session_token)
            except DoesNotExist:
                raise NoSuchSession() from None

    @property
    def account(self):
        """Gets the verified targeted account"""
        account = self.session.account

        if account.root or account.admin:
            su_account = self.query.get('account')

            if su_account is not None:
                try:
                    su_account = Account.find(su_account)
                except DoesNotExist:
                    raise NoSuchAccount() from None
                else:
                    if account.root:
                        return su_account
                    elif su_account.customer == account.customer:
                        return su_account
                    else:
                        raise NotAuthorized() from None

        return account

    @property
    def customer(self):
        """Gets the verified targeted customer"""
        account = self.session.account

        if account.root:
            su_customer = self.query.get('customer')

            if su_customer is not None:
                try:
                    return Customer.find(su_customer)
                except DoesNotExist:
                    raise NoSuchCustomer() from None

        return account.customer


class AuthorizedService(AuthenticatedService):
    """A HIS service that checks whether
    the account is enabled for it
    """

    def _check(self):
        """Determines whether the account
        is allowed to use this service
        """
        try:
            super()._check()
        except CheckPassed:
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
                        #   2) account's customer is enabled for the service
                        #      and
                        #       2a) account is admin or
                        #       2b) account is enabled for the service
                        #
                        account = self.account

                        if account.root:
                            raise CheckPassed() from None
                        elif service in CustomerService.services(
                                account.customer):
                            if account.admin:
                                raise CheckPassed() from None
                            elif service in account.services:
                                raise CheckPassed() from None
                            else:
                                raise NotAuthorized() from None
                        else:
                            raise NotAuthorized() from None


class AdminService(AuthenticatedService):
    """Base class for admin-only services"""

    def _check(self):
        """Check whether we are an admin"""
        try:
            super()._check()
        except CheckPassed:
            if self.account.admin:
                raise CheckPassed()
            else:
                raise NotAuthorized() from None


class RootService(AuthenticatedService):
    """Base class for root-only services"""

    def _check(self):
        """Check whether we are root"""
        try:
            super()._check()
        except CheckPassed:
            if self.account.root:
                raise CheckPassed()
            else:
                raise NotAuthorized() from None
