"""
Handles the request_uri from the environ dictionary
"""
from .session import SessionController
from homeinfo.his.db import User
from homeinfo.his.lib.err import NoSuchUser

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['ResourceController']


class ResourceController():
    """
    Handles resources
    """
    @classmethod
    def handle(cls, resource, params):
        """Checks access rights on the resource for a user"""
        if resource == ['login']:
            hashed_user_name = params.get('user_name', None)
            passwd = params.get('user_pass', None)
            return SessionController.login(hashed_user_name, passwd)
        else:
            uid_str = params.get('uid', None)
            try:
                uid = int(uid_str)
            except:
                raise NoSuchUser()
            session_token = params.get('session_token', None)
            if SessionController.valid(hashed_user_name, session_token):
                user = User.by_id(uid)
                # access_service(