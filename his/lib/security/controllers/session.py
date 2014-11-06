"""
Session management
"""
from his.lib.db import User
from datetime import datetime, timedelta
from uuid import uuid4

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'
__all__ = ['SessionManager', 'AlreadyLoggedIn', 'WrongPassword']

class NoSuchUser(Exception):
    """Indicates that a user does not exist"""
    pass


class AlreadyLoggedIn(Exception):
    """Indicates that a user is already logged in"""
    pass


class WrongPassword(Exception):
    """Indicates that a user provided a wrong password on login"""
    pass


class InvalidSessionToken(Exception):
    """Indicates that a user provided a wrong session token"""
    pass


class AmbiguousUserName(Exception):
    """Indicates an ambiguous user name"""
    pass


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
    __sessions = {}
    """A nested dictionary of active sessions:
    {uid: session_token}"""
        
    @property
    def sessions(self):
        """Returns the currently active sessions"""
        return self.__sessions
    
    def active(self, uid):
        """Determine whether a user is having an active session"""
        return uid in self.sessions
    
    def user(self, name):
        """Fetches a user by its user identifier"""
        users = [u for u in User.select().where(User.name == name)]
        if len(users) == 1:
            return users[0]
        elif len(users) == 0:
            raise NoSuchUser()
        else:
            raise AmbiguousUserName()
                
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
        
    def _chkpwd(self, user, passwd):
        """Verify password of a user"""
        return user.passwd == passwd
        
    def validate(self, uid, session_token):
        """Validate a session by user name"""
        if uid in self.sessions:
            if self.sessions[uid] == session_token:
                return True
            else:
                raise InvalidSessionToken()
        else:
            return False
        
    def login(self, uid, passwd):
        """Login a user"""
        if self.active(uid):
            raise AlreadyLoggedIn(uid)
        else:
            if self.exists(uid):
                user = self.user(uid)
                if self._chkpwd(user, passwd):
                    init_session_token = self._gen_session_token()
                    self._set_session(uid, init_session_token)
                else:
                    raise WrongPassword()
            else:
                raise NoSuchUser()