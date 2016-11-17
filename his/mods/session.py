"""HIS meta services"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, OK, JSON

from his.api.errors import MissingCredentials, InvalidCredentials, \
    NoSessionSpecified, NoSuchSession, SessionExpired, \
    NotAuthorized
from his.api.handlers import HISService
from his.orm import Account, Session

__all__ = [
    'Session',
    'install']


class SessionManager(HISService):
    """Session handling service"""

    NODE = 'session'
    NAME = 'sessions manager'
    DESCRIPTION = 'Manages account sessions'
    PROMOTE = False
    PARAMETER_ERROR = Error(
        'Must specify either account name or session token',
        status=400)

    def get(self):
        """Lists session information"""
        if not self.resource:
            # List all sessions iff specified session is root
            try:
                session = self.query['session']
            except KeyError:
                raise NoSessionSpecified()
            else:
                try:
                    session = Session.get(Session.token == session)
                except DoesNotExist:
                    raise NoSuchSession()
                else:
                    if session.alive:
                        if session.account.root:
                            sessions = {}

                            for session in Session:
                                sessions[session.token] = session.to_dict()

                            return JSON(sessions)
                        else:
                            raise NotAuthorized()
                    else:
                        raise SessionExpired()
        else:
            # List specific session information
            try:
                session = Session.get(Session.token == self.resource)
            except DoesNotExist:
                raise NoSuchSession()
            else:
                if session.alive:
                    return JSON(session.to_dict())
                else:
                    raise SessionExpired()

    def post(self):
        """Handles account login requests"""
        if self.resource is not None:
            raise Error('Sub-sessions are not supported')

        # XXX: Currently ignores posted data
        try:
            account = self.query['account']
            passwd = self.query['passwd']
        except KeyError:
            raise MissingCredentials()
        else:
            try:
                account = Account.get(Account.name == account)
            except DoesNotExist:
                raise InvalidCredentials()
            else:
                session = account.login(passwd)
                return JSON(session.to_dict())

    def put(self):
        """Tries to keep a session alive"""
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()
        else:
            if session.alive:
                if session.renew():
                    return JSON(session.to_dict())
                else:
                    raise SessionExpired()
            else:
                raise SessionExpired()

    def delete(self):
        """Tries to close a specific session identified by its token or
        all sessions for a certain account specified by its name
        """
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()
        else:
            session.close()
            return JSON({'closed': session.token})

    def options(self):
        """Returns the options"""
        return OK()


install = [SessionManager]