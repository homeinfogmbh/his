"""Keeping a session alive"""

from homeinfo.lib.wsgi import Error

from his.api import HISService
from his.orm import Session
from his.crypto import load


class Service(HISService):
    """Handles keepalive requests"""

    def get(self):
        """Tries to keep a session alive"""
        try:
            session_token = self.qd['session_token']
        except KeyError:
            return Error('No session token specified.', status=400)

        try:
            passwd = self.qd['passwd']
        except KeyError:
            return Error('No password specified.', status=400)

        try:
            session = Session.get(Session.token == session_token)
        except DoesNotExist:
            return Error('No such session.', status=400)
        else:
            if session.active:
                if session.renew():
                    return OK('Session has been renewed.')
                else:
                    return Error('Could not renew session.', status=500)
            else:
                return Error('Session has already expired.', status=400)
