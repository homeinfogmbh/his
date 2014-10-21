"""
Session management
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'

__all__ = ['SessionManager', 'AlreadyLoggedIn', 'WrongPassword']

from .user import *
from datetime import datetime, timedelta
from uuid import uuid4

class SessionToken():
    """
    A session token
    """
    __uuid = None
    __deadline = None
    
    def __init__(self, ttl=60, deadline=None):
        """Creates a new session token"""
        self.__uuid = uuid4()
        self.__deadline = deadline if deadline \
            else datetime.now() + timedelta(seconds=ttl)
        
    @property
    def uuid(self):
        """Returns the session token's UUID"""
        return self.__uuid
    
    @property
    def deadline(self):
        """Returns the session token's deadline"""
        return self.__deadline
    
    @property
    def valid(self):
        """Determines whether the session token is (still) valid"""
        return True if self.deadline > datetime.now() else False
        
    def __str__(self):
        """Converts the session token into a string"""
        return self.uuid
    
    def __repr__(self):
        """Converts the session token into a unique string"""
        return self.uuid + '@' + str(self.deadline)
    
    def __eq__(self, other):
        """Equals comparison"""
        if self.valid:
            if type(other) == SessionToken:
                if other.valid:
                    return True if self.uuid == other.uuid else False
                else:
                    return False
            else:
                return True if self.uuid == str(other) else False
        else:
            return False
             
    
class SessionManager():
    """
    Class to manage sessions
    """
    __user_auth = None
    """A user authenticator"""
    __sessions = {}
    """A nested dictionary of active sessions:
    {uid: session_token}"""
    
    def __init__(self):
        """Creates new instance of the session manager"""
        self.__user_auth = UserAuthenticator()
        
    @property
    def user_auth(self):
        """Returns the user authenticator"""
        return self.__user_auth
        
    @property
    def sessions(self):
        """Returns the currently active sessions"""
        return self.__sessions
    
    def active(self, uid):
        """Determine whether a user is having an active session"""
        return uid in self.sessions
                
    def _set_session(self, uid, session_token):
        """Set a session token for a user"""
        self.__sessions[uid] = session_token
        
    def _del_session(self, uid):
        """Delete a session for a user"""
        try:
            del self.__sessions[uid]
        except KeyError:
            return False
        else:
            return True
        
    def validate(self, uid, session_token):
        """Validate a session by user name"""
        if uid in self.sessions:
            if self.sessions[uid] == session_token:
                return True
            else:
                raise InvalidSessionToken()
        else:
            return False
        
    def login(self, uid, passwd, hashfunc=None):
        """Login a user"""
        if self.active(uid):
            raise AlreadyLoggedIn(uid)
        else:
            if self.exists(uid):
                if self._chkpwd(uid, passwd, hashfunc):
                    session_token_ttl = self._gen_session_token()
                    self._set_session(uid, session_token_ttl)
                else:
                    raise WrongPassword()
            else:
                raise NoSuchUser()
        
#===============================================================================
# Exception
#===============================================================================
class AlreadyLoggedIn(Exception):
    """Indicates that a user is already logged in"""
    pass

class WrongPassword(Exception):
    """Indicates that a user provided a wrong password on login"""
    pass

class InvalidSessionToken(Exception):
    """Indicates that a user provided a wrong session token"""
    pass