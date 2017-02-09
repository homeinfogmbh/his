"""Web API errors"""

from json import loads

from homeinfo.lib.wsgi import JSON, InternalServerError

from his.api.locale import Language

__all__ = [
    'HISMessage',
    'HISServerError',
    'IncompleteImplementationError',

    'ServiceError',
    'ServiceNotRegistered',
    'NoServiceSpecified',
    'NoSuchService',

    'HISDataError',
    'NotAnInteger',
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

    'BoundaryError',
    'DurationOutOfBounds']


_IDS = set()


with open('/etc/his.d/locale.json', 'r') as locales:
    _LOCALE = loads(locales.read())


class UniquelyIdentifiedMessage(type):
    """Metaclass for uniquely identified messages"""

    def __init__(self, *args, **kwargs):
        """Checks for non-unique IDs"""
        try:
            my_id = self.ID
        except AttributeError:
            raise InternalServerError(
                'Unidentified message: {}'.format(self)) from None
        else:
            if my_id in _IDS:
                raise InternalServerError(
                    'Ambiguous message ID: {}'.format(my_id)) from None
            else:
                _IDS.add(my_id)
                super().__init__(*args, **kwargs)


class HISMessage(JSON, metaclass=UniquelyIdentifiedMessage):
    """Indicates errors for the WebAPI"""

    ID = None   # Base message

    def __init__(self, *msgs, cors=None, lang=None, **data):
        """Initializes the message"""

        if lang is not None:
            locale = _LOCALE.get(self.ID, {}).get(lang)
        else:
            locale = self.MESSAGE

        if msgs:
            locale.format(*msgs)

        dictionary = {'message': locale}
        dictionary.update(data)

        super().__init__(dictionary, status=self.STATUS, cors=cors)


class HISServerError(HISMessage):
    """Indicates errors for the WebAPI"""

    ID = 100
    STATUS = 500


class IncompleteImplementationError(HISServerError):
    """Indicates an incomplete implementation of the service"""

    ID = 110
    LOCALE = {
        Language.DE_DE: 'Dieser Dienst wurde noch nicht implementiert.',
        Language.EN_US: 'This service has not yet been implemented.'}


class ServiceError(HISServerError):
    """General service error"""

    ID = 120


class ServiceNotRegistered(ServiceError):
    """Indicates that the service is not registered"""

    ID = 121
    LOCALE = {
        Language.DE_DE: 'Dienst ist nicht registriert.',
        Language.EN_US: 'Service is not registered.'}


class NoServiceSpecified(ServiceError):
    """Indicates that no service was specified"""

    ID = 122
    STATUS = 420
    LOCALE = {
        Language.DE_DE: 'Kein Dienst angegeben.',
        Language.EN_US: 'No service specified.'}


class NoSuchService(ServiceError):
    """Indicates that the service does not exist"""

    ID = 123
    STATUS = 404
    LOCALE = {
        Language.DE_DE: 'Kein solcher Dienst.',
        Language.EN_US: 'No such service.'}


class HISDataError(HISMessage):
    """Indicates errors in sent data"""

    ID = 20
    STATUS = 422


class NotAnInteger(HISDataError):
    """Indicates missing credentials"""

    ID = 21
    LOCALE = {
        Language.DE_DE: 'Keine Ganzzahl.',
        Language.EN_US: 'Not an integer.'}


class InvalidUTF8Data(HISDataError):
    """Indicates that the data provided was not UTF-8 text"""

    ID = 22
    LOCALE = {
        Language.DE_DE: 'Fehlerhafte UTF-8 Daten.',
        Language.EN_US: 'Invalid UTF-8 data.'}


class InvalidJSON(HISDataError):
    """Indicates that the JSON data is invalid"""

    ID = 23
    LOCALE = {
        Language.DE_DE: 'Fehlerhaftes JSON Objekt.',
        Language.EN_US: 'Invalid JSON object.'}


class InvalidCustomerID(HISDataError):
    """Indicates that an invalid customer ID was specified"""

    ID = 24
    LOCALE = {
        Language.DE_DE: 'Ungültige Kundennummer angegeben.',
        Language.EN_US: 'Invalid customer ID specified.'}


class HISAPIError(HISMessage):
    """Indicates errors for the WebAPI"""

    ID = 400
    STATUS = 400


class NotAuthorized(HISAPIError):
    """Indicates that the respective entity
    is not authorized to use the service
    """

    ID = 401
    STATUS = 403
    LOCALE = {
        Language.DE_DE: 'Zugriff verweigert.',
        Language.EN_US: 'Not authorized.'}


class LoginError(HISAPIError):
    """Indicates login errors"""

    ID = 410
    STATUS = 401


class MissingCredentials(LoginError):
    """Indicates missing credentials"""

    ID = 411
    LOCALE = {
        Language.DE_DE: 'Benutzername und / oder Passwort nicht angegeben.',
        Language.EN_US: 'Missing credentials.'}


class InvalidCredentials(LoginError):
    """Indicates invalid credentials"""

    ID = 412
    LOCALE = {
        Language.DE_DE: 'Ungültiger Benutzername und / oder Passwort.',
        Language.EN_US: 'Invalid credentials.'}


class AccountLocked(LoginError):
    """Indicates that the account is locked"""

    ID = 413
    STATUS = 423
    LOCALE = {
        Language.DE_DE: 'Account gesperrt.',
        Language.EN_US: 'Account locked.'}


class AlreadyLoggedIn(LoginError):
    """Indicates that the account is already running a session"""

    ID = 414
    STATUS = 409
    LOCALE = {
        Language.DE_DE: 'Bereits angemeldet.',
        Language.EN_US: 'Already logged in.'}


class SessionError(HISAPIError):
    """Indicates errors with sessions"""

    ID = 420


class NoSessionSpecified(SessionError):
    """Indicates a missing session"""

    ID = 421
    STATUS = 420
    LOCALE = {
        Language.DE_DE: 'Keine Sitzung angegeben.',
        Language.EN_US: 'No session specified.'}


class NoSuchSession(SessionError):
    """Indicates that the specified session does not exist"""

    ID = 422
    STATUS = 404
    LOCALE = {
        Language.DE_DE: 'Keine solche Sitzung.',
        Language.EN_US: 'No such session.'}


class SessionExpired(SessionError):
    """Indicates that the specified session has expired"""

    ID = 423
    STATUS = 410
    LOCALE = {
        Language.DE_DE: 'Sitzung abgelaufen.',
        Language.EN_US: 'Session expired.'}


class CustomerError(HISAPIError):
    """Base for errors regarding customers"""

    ID = 430
    STATUS = 404


class NoCustomerSpecified(CustomerError):
    """Indicates that no customer was specified"""

    ID = 431
    STATUS = 420
    LOCALE = {
        Language.DE_DE: 'Keine Kundennummer angegeben.',
        Language.EN_US: 'No customer specified.'}


class NoSuchCustomer(CustomerError):
    """Indicates that the customer does not exist"""

    ID = 432
    STATUS = 404
    LOCALE = {
        Language.DE_DE: 'Kein solcher Kunde.',
        Language.EN_US: 'No such customer.'}


class AccountError(HISAPIError):
    """Base for errors regarding accounts"""

    ID = 440
    STATUS = 404


class NoAccountSpecified(SessionError):
    """Indicates that no account has been specified"""

    ID = 441
    STATUS = 404
    LOCALE = {
        Language.DE_DE: 'Benutzerkonto nicht gefunden.',
        Language.EN_US: 'No such account.'}


class NoSuchAccount(SessionError):
    """Indicates that an account with the specified name does not exist"""

    ID = 442
    STATUS = 404
    LOCALE = {
        Language.DE_DE: 'Benutzerkonto nicht gefunden.',
        Language.EN_US: 'No such account.'}


class BoundaryError(HISAPIError):
    """Base for boundry violation errors"""

    ID = 450
    STATUS = 403


class DurationOutOfBounds(SessionError):
    """Indicates that an out of bounds duration
    was secified on session creation or renewal
    """

    ID = 451
    LOCALE = {
        Language.DE_DE: 'Sitzungsdauer außerhalb des zulässigen Bereichs.',
        Language.EN_US: 'Session duration out of bounds.'}
