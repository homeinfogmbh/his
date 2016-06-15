"""Terminate a session"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, JSON

from his.api import HISService
from his.orm import Session
from his.crypto import load


class Service(HISService):
    """Closes sessions"""

    PARAMETER_ERROR = Error(
        'Must specify either account name or session token', status=400)

    def get(self):
        """Tries to close a specific session identified by its token or
        all sessions for a certain account specified by its name
        """

        session_token = self.query_dict.get('token')
        account_name = self.query_dict.get('account')

        if session_token is not None account_name is not None:
            return self.PARAMETER_ERROR
        elif session_token is not None:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                return Error('No such session.', status=400)
            else:
                session.close()
                return JSON({'sessions_closed': session.token})
        elif account_name is not None:
            try:
                account = Account.get(Account.name == account_name)
            except DoesNotExist:
                return Error('No such account.', status=400)
            else:
                sessions_closed = []

                for session in Session.select().where(
                        Session.account == account):
                    session.close()
                    sessions_closed.append(session.token)

                return JSON({'sessions_closed': sessions_closed})
        else:
            return self.PARAMETER_ERROR
