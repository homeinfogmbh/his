"""Web API errors"""

from homeinfo.lib.wsgi import JSON

from his.locale import Language

__all__ = [
    'HISAPIError',

    'LoginError',
    'MissingCredentials',
    'NoSuchAccount',
    'InvalidCredentials',
    'AlreadyLoggedIn',

    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',

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

    def __init__(self, charset='utf-8', cors=None):
        super().__init__(
            self.LOCALE,
            charset=charset,
            status=self.STATUS,
            cors=cors)


class HISServerError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 500


class HISAPIError(HISMessage):
    """Indicates errors for the WebAPI"""

    STATUS = 400


class LoginError(HISAPIError):
    """Indicates login errors"""

    pass


class MissingCredentials(LoginError):
    """Indicates missing credentials"""

    LOCALE = {
        Language.DE_DE: 'Benutzername und / oder Passwort nicht angegeben.',
        Language.EN_US: 'Missing credentials.'}


class NoSuchAccount(LoginError):
    """Indicates that an account with the specified name does not exist"""

    LOCALE = {
        Language.DE_DE: 'Benutzerkonto nicht gefunden.',
        Language.EN_US: 'No such account.'}


class InvalidCredentials(LoginError):
    """Indicates invalid credentials"""

    LOCALE = {
        Language.DE_DE: 'Ungültiger Benutzername und / oder Passwort.',
        Language.EN_US: 'Invalid credentials.'}


class AlreadyLoggedIn(LoginError):
    """Indicates that the account is already running a session"""

    LOCALE = {
        Language.DE_DE: 'Bereits angemeldet.',
        Language.EN_US: 'Already logged in.'}


class SessionError(HISAPIError):
    """Indicates errors with sessions"""

    pass


class NoSessionSpecified(SessionError):
    """Indicates a missing session"""

    LOCALE = {
        Language.DE_DE: 'Keine Sitzung angegeben.',
        Language.EN_US: 'No session specified.'}


class NoSuchSession(SessionError):
    """Indicates that the specified session does not exist"""

    LOCALE = {
        Language.DE_DE: 'Keine solche Sitzung.',
        Language.EN_US: 'No such session.'}


class SessionExpired(SessionError):
    """Indicates that the specified session has expired"""

    LOCALE = {
        Language.DE_DE: 'Sitzung abgelaufen.',
        Language.EN_US: 'Session expired.'}


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


class NoSuchService(ServiceError):
    """Indicates that the service does not exist"""

    LOCALE = {
        Language.DE_DE: 'Kein solcher Dienst.',
        Language.EN_US: 'No such service.'}


class CustomerError(HISAPIError):
    """Indicates errors with customers"""

    pass


class NoCustomerSpecified(ServiceError):
    """Indicates that no customer was specified"""

    LOCALE = {
        Language.DE_DE: 'Keine Kundennummer angegeben.',
        Language.EN_US: 'No customer specified.'}


class InvalidCustomerID(ServiceError):
    """Indicates that an invalid customer ID was specified"""

    LOCALE = {
        Language.DE_DE: 'Ungültige Kundennummer angegeben.',
        Language.EN_US: 'Invalid customer ID specified.'}


class NoSuchCustomer(CustomerError):
    """Indicates that the customer does not exist"""

    LOCALE = {
        Language.DE_DE: 'Kein solcher Kunde.',
        Language.EN_US: 'No such customer.'}


class NotAuthorized(HISAPIError):
    """Indicates that the respective entity
    is not authorized to use the service
    """

    LOCALE = {
        Language.DE_DE: 'Zugriff verweigert.',
        Language.EN_US: 'Not authorized.'}
