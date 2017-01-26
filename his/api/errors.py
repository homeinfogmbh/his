"""Web API errors"""

from homeinfo.lib.wsgi import JSON

from his.api.locale import Language

__all__ = [
    'HISAPIError',
    'IncompleteImplementationError',
    'NotAnInteger',

    'LoginError',
    'MissingCredentials',
    'InvalidCredentials',
    'AccountLocked',
    'AlreadyLoggedIn',

    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'NoSuchAccount',
    'DurationOutOfBounds',

    'ServiceError',
    'ServiceNotRegistered',
    'NoServiceSpecified',
    'NoSuchService',

    'CustomerError',
    'NoCustomerSpecified',
    'InvalidCustomerID',
    'NoSuchCustomer',

    'NotAuthorized']


class HISMessage(JSON):
    """Indicates errors for the WebAPI"""

    def __init__(self, charset='utf-8', cors=None, status=None, data=None):
        """Initializes the message"""
        status = self.STATUS if status is None else status
        dictionary = {}

        for key in self.LOCALE:
            dictionary[key] = self.LOCALE[key]

        if data is not None:
            for key in data:
                dictionary[key] = data[key]

        super().__init__(
            dictionary,
            charset=charset,
            status=status,
            cors=cors)


class HISServerError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 500


class HISAPIError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 400


class IncompleteImplementationError(HISAPIError):
    """Indicates an incomplete implementation of the service"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Dieser Dienst wurde noch nicht implementiert.',
        Language.EN_US: 'This service has not yet been implemented.'}


class LoginError(HISAPIError):
    """Indicates login errors"""

    STATUS = 401


class NotAnInteger(HISMessage):
    """Indicates missing credentials"""

    LOCALE = {
        Language.DE_DE: 'Keine Ganzzahl.',
        Language.EN_US: 'Not an integer.'}
    STATUS = 422

    def __init__(self, key, value, charset='utf-8', cors=None, status=None):
        """Initializes the message"""
        super().__init__(charset=charset, cors=cors, status=status,
                         data={'key': key, 'value': value})


class MissingCredentials(LoginError):
    """Indicates missing credentials"""

    LOCALE = {
        Language.DE_DE: 'Benutzername und / oder Passwort nicht angegeben.',
        Language.EN_US: 'Missing credentials.'}


class InvalidCredentials(LoginError):
    """Indicates invalid credentials"""

    LOCALE = {
        Language.DE_DE: 'Ungültiger Benutzername und / oder Passwort.',
        Language.EN_US: 'Invalid credentials.'}


class AccountLocked(LoginError):
    """Indicates that the account is locked"""

    LOCALE = {
        Language.DE_DE: 'Account gesperrt.',
        Language.EN_US: 'Account locked.'}
    STATUS = 423


class AlreadyLoggedIn(LoginError):
    """Indicates that the account is already running a session"""

    LOCALE = {
        Language.DE_DE: 'Bereits angemeldet.',
        Language.EN_US: 'Already logged in.'}
    STATUS = 409


class SessionError(HISAPIError):
    """Indicates errors with sessions"""

    pass


class NoSessionSpecified(SessionError):
    """Indicates a missing session"""

    LOCALE = {
        Language.DE_DE: 'Keine Sitzung angegeben.',
        Language.EN_US: 'No session specified.'}
    STATUS = 420


class NoSuchSession(SessionError):
    """Indicates that the specified session does not exist"""

    LOCALE = {
        Language.DE_DE: 'Keine solche Sitzung.',
        Language.EN_US: 'No such session.'}
    STATUS = 404


class SessionExpired(SessionError):
    """Indicates that the specified session has expired"""

    LOCALE = {
        Language.DE_DE: 'Sitzung abgelaufen.',
        Language.EN_US: 'Session expired.'}
    STATUS = 410


class NoSuchAccount(SessionError):
    """Indicates that an account with the specified name does not exist"""

    LOCALE = {
        Language.DE_DE: 'Benutzerkonto nicht gefunden.',
        Language.EN_US: 'No such account.'}
    STATUS = 404


class DurationOutOfBounds(SessionError):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal
    """

    LOCALE = {
        Language.DE_DE: 'Sitzungsdauer außerhalb des zulässigen Bereichs.',
        Language.EN_US: 'Session duration out of bounds.'}
    STATUS = 422


class ServiceError(HISAPIError):
    """General service error"""

    pass


class ServiceNotRegistered(ServiceError):
    """Indicates that the service is not registered"""

    STATUS = 500
    LOCALE = {
        Language.DE_DE: 'Dienst ist nicht registriert.',
        Language.EN_US: 'Service is not registered.'}


class NoServiceSpecified(ServiceError):
    """Indicates that no service was specified"""

    LOCALE = {
        Language.DE_DE: 'Kein Dienst angegeben.',
        Language.EN_US: 'No service specified.'}
    STATUS = 420


class NoSuchService(ServiceError):
    """Indicates that the service does not exist"""

    LOCALE = {
        Language.DE_DE: 'Kein solcher Dienst.',
        Language.EN_US: 'No such service.'}
    STATUS = 404


class CustomerError(HISAPIError):
    """Indicates errors with customers"""

    pass


class NoCustomerSpecified(ServiceError):
    """Indicates that no customer was specified"""

    LOCALE = {
        Language.DE_DE: 'Keine Kundennummer angegeben.',
        Language.EN_US: 'No customer specified.'}
    STATUS = 420


class InvalidCustomerID(ServiceError):
    """Indicates that an invalid customer ID was specified"""

    LOCALE = {
        Language.DE_DE: 'Ungültige Kundennummer angegeben.',
        Language.EN_US: 'Invalid customer ID specified.'}
    STATUS = 406


class NoSuchCustomer(CustomerError):
    """Indicates that the customer does not exist"""

    LOCALE = {
        Language.DE_DE: 'Kein solcher Kunde.',
        Language.EN_US: 'No such customer.'}
    STATUS = 404


class NotAuthorized(HISAPIError):
    """Indicates that the respective entity
    is not authorized to use the service
    """

    LOCALE = {
        Language.DE_DE: 'Zugriff verweigert.',
        Language.EN_US: 'Not authorized.'}
    STATUS = 403
