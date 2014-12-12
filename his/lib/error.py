"""
Handles service access
"""
import pcp

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['Error']


class Error(Exception):
    """
    An error that can be rendered as a PCP exception
    """
    def __init__(self, code, msg):
        """Initializes with a code and a message"""
        self.__code = code
        self.__msg = msg

    @property
    def code(self):
        """Returns the error code"""
        return self.__code

    @property
    def msg(self):
        """Returns the error message"""
        return self.__msg

    @property
    def lang(self):
        """Returns the error description dictionary"""
        try:
            return self._lang
        except AttributeError:
            return {}

    def __pcp__(self):
        """Converts the message to a PCP Error"""
        rsp = pcp.rsp()
        msg = pcp.Message()
        msg.code = self.code
        msg.msg = self.msg
        for lang, text in self.lang.items():
            t = pcp.MessageText(text)
            t.lang = lang
            msg.text.append(t)
        rsp.msg = msg
        rsp.signal = pcp.Signal.NACK    # @UndefinedVariable
        return rsp

    def __xml__(self):
        """Renders itself as a PCP message to XML bytes"""
        return self.__pcp__().toxml(encoding='utf-8')

    def __json__(self):
        """Renders itself as a PCP message to JSON bytes"""
        return self.__pcp__().tojson(encoding='utf-8')

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


class InvalidCredentials(Error):
    """Indicates that a user tried to
    log in with invalid credentials"""
    _lang = {'EN': 'User name and / or password are invalid.',
             'DE': 'Benutzername und / oder Passwort ungültig.'}

    def __init__(self):
        super().__init__(1, 'INVALID_CREDENTIALS')


class SessionTimeout(Error):
    """Indicates that a user's session has times out"""
    _lang = {'EN': 'Session timed out.',
             'DE': 'Sitzung abgelaufen.'}

    def __init__(self):
        super().__init__(2, 'SESSION_TIMED_OUT')


class SessionExists(Error):
    """Indicates that a session for
    a user is already running"""
    _lang = {'EN': 'You are already logged in.',
             'DE': 'Sie sind bereits angemeldet.'}

    def __init__(self):
        super().__init__(3, 'SESSION_EXISTS')


class UserLocked(Error):
    """Indicates that a user has been locked"""
    _lang = {'EN': 'User account locked.',
             'DE': 'Benutzerkonto gesperrt.'}

    def __init__(self):
        super().__init__(4, 'USER_LOCKED')


class NotLoggedIn(Error):
    """Indicates that a user has no active session"""
    _lang = {'EN': 'You are not logged in.',
             'DE': 'Sie sind nicht angemeldet.'}

    def __init__(self):
        super().__init__(5, 'NOT_LOGGED_IN')


class NoSuchService(Error):
    """Indicates that a service does not exist"""
    _lang = {'EN': 'The requested service does not exist.',
             'DE': 'Der angeforderte Dienst existiert nicht.'}

    def __init__(self):
        super().__init__(6, 'NO_SUCH_SERVICE')


class UnauthorizedUser(Error):
    """Indicates that a user is not
    allowed to access a service"""
    _lang = {'EN': 'You are not allowed to access the requested resource.',
             'DE': 'Sie sind nicht berechtigt, auf die'
             'angeforderte Ressource zuzugreifen.'}

    def __init__(self):
        super().__init__(7, 'UNAUTHORIZED_USER')


class UnauthorizedGroup(Error):
    """Indicates that a group is not
    allowed to access a service"""
    _lang = {'EN': 'Your group are not allowed to'
             'access the requested resource.',
             'DE': 'Ihre Gruppe ist nicht berechtigt, auf die'
             'angeforderte Ressource zuzugreifen.'}

    def __init__(self):
        super().__init__(8, 'UNAUTHORIZED_GROUP')


class NotAuthenticated(Error):
    """Indicates that a protected resource was
    accessed without authentication information"""
    _lang = {'EN': 'Go away!',
             'DE': 'Geh weg!'}

    def __init__(self):
        super().__init__(9, 'NOT_AUTHENTICATED')


class NotAuthorized(Error):
    """Indicates that a protected resource was
    accessed without authorization information"""
    _lang = {'EN': 'Go away!',
             'DE': 'Geh weg!'}

    def __init__(self):
        super().__init__(10, 'NOT_AUTHORIZED')


class InternalServerError(Error):
    """Indicates that an unexpected error
    occurred within the system"""
    _lang = {'EN': 'Internal server error.',
             'DE': 'Interner Server-Fehler.'}

    def __init__(self):
        super().__init__(11, 'INTERNAL_SERVER_ERROR')


class NoSuchResource(Error):
    """Indicates that a non-existent
    resource has been requested"""
    _lang = {'EN': 'No such resource.',
             'DE': 'Keine solche Ressource.'}

    def __init__(self):
        super().__init__(12, 'NO_SUCH_RESOURCE')


class UnsupportedAction(Error):
    """Indicates that an unsupported action
    (GET, POST, PUT, DELETE)
    has been tried to apply on a certain resource"""
    _lang = {'EN': 'Unsupported action.',
             'DE': 'Nicht-unterstützte Aktion.'}

    def __init__(self):
        super().__init__(13, 'UNSUPPORTED_ACTION')
