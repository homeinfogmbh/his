"""Web API errors"""

from homeinfo.lib.wsgi import JSON

__all__ = [
    'HISAPIError',
    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'ServiceNotRegistered',
    'NotAuthorized']


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
