"""Web API errors"""

from contextlib import suppress
from configparser import ConfigParser
from homeinfo.lib.wsgi import JSON

__all__ = [
    'HISMessage',
    'HISServerError',
    'IncompleteImplementationError',

    'ServiceError',
    'ServiceNotRegistered',
    'NoServiceSpecified',
    'NoSuchService',

    'HISDataError',
    'NoDataProvided',
    'NotAnInteger',
    'InvalidData',
    'InvalidUTF8Data',
    'InvalidJSON',
    'InvalidCustomerID',

    'HISAPIError',
    'NotAuthorized',
    'LoginError',
    'MissingCredentials',
    'InvalidCredentials',
    'AccountLocked',
    'AlreadyLoggedIn',

    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',

    'CustomerError',
    'NoCustomerSpecified',
    'NoSuchCustomer',

    'AccountError',
    'NoAccountSpecified',
    'NoSuchAccount',
    'AccountPatched',

    'BoundaryError',
    'DurationOutOfBounds']


class HISMessage(JSON):
    """Indicates errors for the WebAPI"""

    STATUS = 200
    LOCALE = ConfigParser()
    LOCALE.read('/etc/his.d/locale/core.ini')

    def __init__(self, *data, cors=None, lang='de_DE', **fields):
        """Initializes the message"""

        with suppress(KeyError):
            locale = self.LOCALE[self.__class__.__name__][lang]

        if data:
            locale.format(*data)

        dictionary = {'message': locale}
        dictionary.update(fields)

        super().__init__(dictionary, status=self.STATUS, cors=cors)


class HISServerError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 500


class IncompleteImplementationError(HISServerError):
    """Indicates an incomplete implementation of the service"""

    pass


class ServiceError(HISServerError):
    """General service error"""

    pass


class ServiceNotRegistered(ServiceError):
    """Indicates that the service is not registered"""

    pass


class NoServiceSpecified(ServiceError):
    """Indicates that no service was specified"""

    STATUS = 420


class NoSuchService(ServiceError):
    """Indicates that the service does not exist"""

    STATUS = 404


class HISDataError(HISMessage):
    """Indicates errors in sent data"""

    STATUS = 422


class NoDataProvided(HISDataError):
    """Indicates missing data"""

    pass


class NotAnInteger(HISDataError):
    """Indicates missing credentials"""

    pass


class InvalidData(HISDataError):
    """Indicates missing data"""

    pass


class InvalidUTF8Data(InvalidData):
    """Indicates that the data provided was not UTF-8 text"""

    pass


class InvalidJSON(InvalidData):
    """Indicates that the JSON data is invalid"""

    pass


class InvalidCustomerID(InvalidData):
    """Indicates that an invalid customer ID was specified"""

    pass


class HISAPIError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 400


class NotAuthorized(HISAPIError):
    """Indicates that the respective entity
    is not authorized to use the service
    """

    STATUS = 403


class LoginError(HISAPIError):
    """Indicates login errors"""

    STATUS = 401


class MissingCredentials(LoginError):
    """Indicates missing credentials"""

    pass


class InvalidCredentials(LoginError):
    """Indicates invalid credentials"""

    pass


class AccountLocked(LoginError):
    """Indicates that the account is locked"""

    STATUS = 423


class AlreadyLoggedIn(LoginError):
    """Indicates that the account is already running a session"""

    STATUS = 409


class SessionError(HISAPIError):
    """Indicates errors with sessions"""

    pass


class NoSessionSpecified(SessionError):
    """Indicates a missing session"""

    STATUS = 420


class NoSuchSession(SessionError):
    """Indicates that the specified session does not exist"""

    STATUS = 404


class SessionExpired(SessionError):
    """Indicates that the specified session has expired"""

    STATUS = 410


class DurationOutOfBounds(SessionError):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal
    """

    pass


class CustomerError(HISAPIError):
    """Base for errors regarding customers"""

    STATUS = 404


class NoCustomerSpecified(CustomerError):
    """Indicates that no customer was specified"""

    STATUS = 420


class NoSuchCustomer(CustomerError):
    """Indicates that the customer does not exist"""

    STATUS = 404


class AccountError(HISAPIError):
    """Base for errors regarding accounts"""

    STATUS = 404


class NoAccountSpecified(AccountError):
    """Indicates that no account has been specified"""

    STATUS = 404


class NoSuchAccount(AccountError):
    """Indicates that an account with the specified name does not exist"""

    STATUS = 404


class AccountPatched(AccountError):
    """Indicates that the account has been patched successfully"""

    STATUS = 200


class BoundaryError(HISAPIError):
    """Base for boundry violation errors"""

    STATUS = 403
