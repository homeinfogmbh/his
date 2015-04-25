"""Error messages for the external WSGI interface"""

from pcp import pcp

__all__ = ['InterfaceError']


# TODO: Let HTTP errors be handles by homeinfolib.wsgi.Error

class InterfaceError(Exception):
    """An error that can be rendered as a PCP exception"""

    def __init__(self, code, msg, desc, http_status=None):
        """Initializes with a code and a message"""
        self._code = code
        self._msg = msg
        self._desc = desc
        self._http_status = http_status or 500

    @property
    def code(self):
        """Returns the error code"""
        return self._code

    @property
    def msg(self):
        """Returns the error message"""
        return self._msg

    @property
    def desc(self):
        """Returns the error description dictionary"""
        return self._desc

    @property
    def http_status(self):
        """Returns the HTTP status code"""
        return self._http_status

    def __dom__(self):
        """Converts the message to a DOM model"""
        rsp = pcp.pcp()
        msg = pcp.Message()
        msg.code = self.code
        msg.msg = self.msg
        for lang, text in self.desc.items():
            t = pcp.MessageText(text)
            t.lang = lang
            msg.text.append(t)
        rsp.msg = msg
        rsp.signal = pcp.Signal.NACK    # @UndefinedVariable
        return rsp

    def __xml__(self):
        """Renders itself as a PCP message to XML bytes"""
        return self.__dom__().toxml(encoding='utf-8')

    def __json__(self):
        """Renders itself as a PCP message to JSON bytes"""
        return self.__dom__().tojson(encoding='utf-8')

    def __int__(self):
        """Returns the error code number"""
        return self.code

    def __str__(self):
        """Converts the message to a PCP Error XML string"""
        return self.__xml__().decode()

    def __eq__(self, other):
        """Equality comparison"""
        return int(self) == int(other)

    def __gt__(self, other):
        """Greater-than comparison"""
        return int(self) > int(other)

    def __ge__(self, other):
        """Greater-than comparison"""
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        """Greater-than comparison"""
        return int(self) < int(other)

    def __le__(self, other):
        """Greater-than comparison"""
        return self.__lt__(other) or self.__eq__(other)


class InvalidCredentials(InterfaceError):
    """Indicates that a user tried to
    log in with invalid credentials
    """

    def __init__(self):
        super().__init__(1, 'INVALID_CREDENTIALS',
                         {'EN': 'User name and / or password are invalid.',
                          'DE': 'Benutzername und / oder Passwort ungültig.'},
                         http_status=400)


class SessionTimeout(InterfaceError):
    """Indicates that a user's session has times out"""

    def __init__(self):
        super().__init__(2, 'SESSION_TIMED_OUT',
                         {'EN': 'Session timed out.',
                          'DE': 'Sitzung abgelaufen.'},
                         http_status=403)


class SessionExists(InterfaceError):
    """Indicates that a session for
    a user is already running
    """

    def __init__(self):
        super().__init__(3, 'SESSION_EXISTS',
                         {'EN': 'You are already logged in.',
                          'DE': 'Sie sind bereits angemeldet.'},
                         http_status=400)


class UserLocked(InterfaceError):
    """Indicates that a user has been locked"""

    def __init__(self):
        super().__init__(4, 'USER_LOCKED',
                         {'EN': 'User account locked.',
                          'DE': 'Benutzerkonto gesperrt.'},
                         http_status=403)


class NotLoggedIn(InterfaceError):
    """Indicates that a user has no active session"""

    def __init__(self):
        super().__init__(5, 'NOT_LOGGED_IN',
                         {'EN': 'You are not logged in.',
                          'DE': 'Sie sind nicht angemeldet.'},
                         http_status=403)


class NoSuchService(InterfaceError):
    """Indicates that a service does not exist"""

    def __init__(self):
        super().__init__(6, 'NO_SUCH_SERVICE',
                         {'EN': 'The requested service does not exist.',
                          'DE': 'Der angeforderte Dienst existiert nicht.'},
                         http_status=404)


class UnauthorizedUser(InterfaceError):
    """Indicates that a user is not
    allowed to access a service
    """

    def __init__(self):
        super().__init__(7, 'UNAUTHORIZED_USER',
                         {'EN': 'You are not allowed to access'
                          ' the requested resource.',
                          'DE': 'Sie sind nicht berechtigt, auf die'
                          ' angeforderte Ressource zuzugreifen.'},
                         http_status=401)


class UnauthorizedGroup(InterfaceError):
    """Indicates that a group is not
    allowed to access a service
    """

    def __init__(self):
        super().__init__(8, 'UNAUTHORIZED_GROUP',
                         {'EN': 'Your group are not allowed to'
                          'access the requested resource.',
                          'DE': 'Ihre Gruppe ist nicht berechtigt, auf die'
                          'angeforderte Ressource zuzugreifen.'},
                         http_status=401)


class NotAuthenticated(InterfaceError):
    """Indicates that a protected resource was
    accessed without authentication information
    """

    def __init__(self):
        super().__init__(9, 'NOT_AUTHENTICATED',
                         {'EN': 'Go away!',
                          'DE': 'Geh weg!'},
                         http_status=403)


class NotAuthorized(InterfaceError):
    """Indicates that a protected resource was
    accessed without authorization information
    """

    def __init__(self):
        super().__init__(10, 'NOT_AUTHORIZED',
                         {'EN': 'Go away!',
                          'DE': 'Geh weg!'},
                         http_status=401)


class InternalServerError(InterfaceError):
    """Indicates that an unexpected error
    occurred within the system
    """

    def __init__(self):
        super().__init__(11, 'INTERNAL_SERVER_ERROR',
                         {'EN': 'Internal server error.',
                          'DE': 'Interner Server-Fehler.'},
                         http_status=500)


class NoSuchResource(InterfaceError):
    """Indicates that a non-existent
    resource has been requested
    """

    def __init__(self):
        super().__init__(12, 'NO_SUCH_RESOURCE',
                         {'EN': 'No such resource.',
                          'DE': 'Keine solche Ressource.'},
                         http_status=404)


class UnsupportedHTTPAction(InterfaceError):
    """Indicates that an unsupported action
    (GET, POST, PUT, DELETE)
    has been tried to apply on a certain resource
    """

    def __init__(self):
        super().__init__(13, 'UNSUPPORTED_HTTP_ACTION',
                         {'EN': 'Unsupported HTTP action.',
                          'DE': 'Nicht-unterstützte HTTP-Aktion.'},
                         http_status=405)
