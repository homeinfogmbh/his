"""Meta-services for HIS"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, RequestHandler

from his.orm import Service, CustomerService, Session

__all__ = [
    'IncompleteImplementationError',
    'HISAPIError',
    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'HISService',
    'SessionService',
    'AccountService',
    'CheckedAccountService']


class IncompleteImplementationError(NotImplementedError):
    """Indicates an incomplete implementation of the service"""

    pass


class HISAPIError(JSON):
    """Indicates errors for the WebAPI"""

    def __init__(self, charset='utf-8', cors=None):
        super().__init__(
            self.LOCALE,
            charset=charset,
            status=self.STATUS,
            cors=cors)


class SessionError(HISAPIError):
    """Indicates errors with sessions"""

    pass


class NoSessionSpecified(SessionError):
    """Indicates a missing session"""

    STATUS = 400

    LOCALE = {
        'de_DE': 'Keine Sitzung angegeben.',
        'en_US': 'No session specified.'}


class NoSuchSession(SessionError):
    """Indicates that the specified session does not exist"""

    STATUS = 400

    LOCALE = {
        'de_DE': 'Keine solche Sitzung.',
        'en_US': 'No such session.'}


class SessionExpired(SessionError):
    """Indicates that the specified session has expired"""

    STATUS = 400

    LOCALE = {
        'de_DE': 'Sitzung abgelaufen.',
        'en_US': 'Session expired.'}


class ServiceNotRegistered(HISAPIError):
    """Indicates that the service is not registered"""

    STATUS = 500

    LOCALE = {
        'de_DE': 'Dienst ist nicht registriert.',
        'en_US': 'Service is not registered.'}


class NotAuthorized(HISAPIError):
    """Indicates that the respective entity
    is not authorized to use the service
    """

    STATUS = 400

    LOCALE = {
        'de_DE': 'Zugriff verweigert.',
        'en_US': 'Not authorized.'}


class HISService(RequestHandler):
    """A generic HIS service"""

    PATH = None
    NAME = None
    DESCRIPTION = None
    PROMOTE = None

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


class SessionService(HISService):
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


class AccountService(SessionService):
    """A HIS service that is account- and customer-aware"""

    @property
    def account(self):
        """Returns the respective account"""
        return self.session.account

    @property
    def customer(self):
        """Returns the respective customer"""
        return self.session.account.customer


class CheckedAccountService(AccountService):
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
