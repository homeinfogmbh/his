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
        if deadline:
            self.__deadline = deadline
        else:
            self.__deadline = datetime.now() + timedelta(seconds=ttl)
        
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
        return self.uuid + ' ' + str(self.deadline)
    
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
    {user_name: {session_token: timeout}}"""
    
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
    
    def active(self, user_name):
        """Determine whether a user is having an active session"""
        for user in self.sessions:
            if user == user_name:
                return True
        return False
                
    def _set_session(self, user_name, session_token_ttl):
        """Set a session token and TTL in seconds for a user"""
        self.__sessions[user_name] = session_token_ttl
        
    def _gen_session_token(self, ttl=60):
        """Generates a session token"""
        return {uuid4(): datetime.now() + timedelta(seconds=ttl)}
        
    def validate(self, user_name, session_token):
        """Validate a session by user name"""
        for session in self.sessions:
            if session == user_name:
                for token in session:
                    if token == session_token:
                        return True
                # No session token match
                return False
            else:
                # User not logged in
                return False
        # No sessions
        return False
        
    def login(self, user_name, passwd, hashfunc=None):
        """Login a user"""
        if self.active(user_name):
            raise AlreadyLoggedIn(user_name)
        else:
            if self.exists(user_name):
                if self._chkpwd(user_name, passwd, hashfunc):
                    session_token_ttl = self._gen_session_token()
                    self._set_session(user_name, session_token_ttl)
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