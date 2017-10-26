"""Meta-services for HIS."""

from contextlib import suppress

from peewee import DoesNotExist

from homeinfo.crm import Customer
from wsgilib import InternalServerError, ResourceHandler

from his.api.messages import IncompleteImplementationError, NotAnInteger, \
    NoSessionSpecified, NoSuchSession, SessionExpired, ServiceNotRegistered, \
    NotAuthorized, NoSuchCustomer, NoSuchAccount, NoDataProvided, \
    InvalidUTF8Data, InvalidJSON
from his.orm import Service, CustomerService, Account, Session

__all__ = [
    'HISService',
    'AuthenticatedService',
    'AuthorizedService',
    'AdminService',
    'RootService']


def check_hook(method):
    """Decorator to mark a method as a check hook."""

    method.check_hook = True
    return method


class HISService(ResourceHandler):
    """A generic HIS service."""

    NODE = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

    ERRORS = {
        'NO_DATA_PROVIDED': NoDataProvided(),
        'NON_UTF8_DATA': InvalidUTF8Data(),
        'NON_JSON_DATA': InvalidJSON()}

    def __call__(self):
        """Checks all check hooks of superclasses and this class in
        order to determine whether the service should be run.
        """
        if all(check_hook(self) for check_hook in self.__check_hooks):
            return super().__call__()

        raise InternalServerError('Service check failed.') from None

    @classmethod
    def install(cls):
        """Installs the service into the database index."""
        if cls.NODE is None or cls.NAME is None:
            raise IncompleteImplementationError() from None

        try:
            service = Service.get(Service.node == cls.NODE)
        except DoesNotExist:
            service = Service()
            service.name = cls.NAME
            service.node = cls.NODE
            service.module = cls.__module__
            service.handler = cls.__name__
            service.description = cls.DESCRIPTION
            service.promote = cls.PROMOTE
            service.save()
            return service

        if service.name == cls.NAME:
            if service.module == cls.__module__:
                if service.handler == cls.__name__:
                    return service

        return False

    @property
    def __check_hooks(self):
        """Yields all check hooks of the superclasses and this class
        in reversed __mro__ order ensuring a top-down test.
        """
        for superclass in reversed(self.__class__.__mro__):
            for name in dir(superclass):
                attribute = getattr(superclass, name)

                with suppress(AttributeError):
                    if attribute.check_hook:
                        print('Yielding check hook', attribute, 'on', self)
                        yield attribute


class AuthenticatedService(HISService):
    """A HIS service that is session-aware."""

    @check_hook
    def check(self):
        """Checks whether the account is logged in."""
        if self.session.alive:
            return True

        raise SessionExpired() from None

    @property
    def session(self):
        """Returns the session or raises an error."""
        try:
            session_token = self.query['session']
        except KeyError:
            raise NoSessionSpecified() from None

        try:
            return Session.get(Session.token == session_token)
        except DoesNotExist:
            raise NoSuchSession() from None

    @property
    def account(self):
        """Gets the verified targeted account."""
        account = self.session.account

        if account.root or account.admin:
            su_account = self.query.get('account')

            if su_account is not None:
                try:
                    su_account = Account.find(su_account)
                except DoesNotExist:
                    raise NoSuchAccount() from None

                if account.root:
                    return su_account
                elif su_account.customer == account.customer:
                    return su_account

                raise NotAuthorized() from None

        return account

    @property
    def customer(self):
        """Gets the verified targeted customer."""
        account = self.session.account

        if account.root:
            su_customer = self.query.get('customer')

            if su_customer is not None:
                try:
                    cid = int(su_customer)
                except ValueError:
                    raise NotAnInteger() from None

                try:
                    return Customer.get(Customer.id == cid)
                except DoesNotExist:
                    raise NoSuchCustomer() from None

        return account.customer


class AuthorizedService(AuthenticatedService):
    """A HIS service that checks whether
    the account is enabled for it.
    """

    @check_hook
    def check(self):
        """Determines whether the account
        is allowed to use this service.
        """
        try:
            node = self.__class__.NODE
        except AttributeError:
            raise IncompleteImplementationError() from None

        if not node:
            raise IncompleteImplementationError() from None

        try:
            service = Service.get(Service.node == node)
        except DoesNotExist:
            raise ServiceNotRegistered() from None

        # Allow call iff
        #   1) account is root or
        #   2) account's customer is enabled for the service
        #      and
        #       2a) account is admin or
        #       2b) account is enabled for the service
        #
        account = self.account

        if account.root:
            return True
        elif service in CustomerService.services(account.customer):
            if account.admin:
                return True
            elif service in account.services:
                return True

        raise NotAuthorized() from None


class AdminService(AuthenticatedService):
    """Base class for admin-only services."""

    @check_hook
    def check(self):
        """Check whether we are an admin."""
        if self.account.admin:
            return True

        raise NotAuthorized() from None


class RootService(AuthenticatedService):
    """Base class for root-only services."""

    @check_hook
    def check(self):
        """Check whether we are root."""
        if self.account.root:
            return True

        raise NotAuthorized() from None
