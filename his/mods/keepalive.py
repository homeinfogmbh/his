"""Keeping a session alive"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, JSON

from his.api import HISService
from his.orm import Session
from his.crypto import load


class Handler(HISService):
    """Handles keepalive requests"""

    def get(self):
        """Tries to keep a session alive"""
        try:
            session_token = self.query_dict['session']
        except KeyError:
            return Error('No session token specified.', status=400)
        else:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                return Error('No such session.', status=400)
            else:
                if session.active:
                    if session.renew():
                        return JSON(session.todict())
                    else:
                        return Error('Could not renew session.', status=500)
                else:
                    return Error('Session has already expired.', status=400)
