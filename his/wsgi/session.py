"""HIS session service."""

from peewee import DoesNotExist

from wsgilib import Error, OK, JSON

from his.api.messages import MissingCredentials, InvalidCredentials, \
    NoSessionSpecified, NoSuchSession, SessionExpired, NotAuthorized, \
    NotAnInteger
from his.api.handlers import service, HISService
from his.orm import Account, Session

__all__ = ['Session', 'INSTALL']


@service('session')
class SessionManager(HISService):
    """Session handling service."""

    PARAMETER_ERROR = Error(
        'Must specify either account name or session token.',
        status=400)

    @property
    def duration(self):
        """Returns the repsective session duration in minutes."""
        duration = self.query.get('duration', 15)

        try:
            return int(duration)
        except (ValueError, TypeError):
            raise NotAnInteger('duration', duration) from None

    def list_sessions(self):
        """Lists all sessions iff specified session is root."""
        try:
            session = self.query['session']
        except KeyError:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == session)
        except DoesNotExist:
            raise NoSuchSession()

        if session.alive:
            if session.account.root:
                sessions = {}

                for session in Session:
                    sessions[session.token] = session.to_dict()

                return JSON(sessions)

            raise NotAuthorized()

        raise SessionExpired()

    def list_session(self):
        """Lists the respective session."""
        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()

        if session.alive:
            return JSON(session.to_dict())

        raise SessionExpired()

    def get(self):
        """Lists session information."""
        if not self.resource:
            return self.list_sessions()

        return self.list_session()

    def post(self):
        """Handles account login requests."""
        if self.resource is not None:
            raise Error('Sub-sessions are not supported.')

        account = self.data.json.get('account')
        passwd = self.data.json.get('passwd')

        if not account or not passwd:
            raise MissingCredentials()

        try:
            account = Account.get(Account.name == account)
        except DoesNotExist:
            raise InvalidCredentials()

        if account.login(passwd):
            session = Session.open(account, duration=self.duration)
            return JSON(session.to_dict())

        raise InvalidCredentials()

    def put(self):
        """Tries to keep a session alive."""
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()

        if session.renew(duration=self.duration):
            return JSON(session.to_dict())

        raise SessionExpired()

    def delete(self):
        """Tries to close a specific session identified by its token or
        all sessions for a certain account specified by its name.
        """
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()

        session.close()
        return JSON({'closed': session.token})

    def options(self):
        """Returns the options."""
        return OK()


INSTALL = [SessionManager]
