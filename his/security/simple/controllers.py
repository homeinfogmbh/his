"""
User authentication
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'

from his.db.tables.passwd import User
from datetime import datetime, timedelta
from uuid import uuid4

class UserAuthenticator():
    """
    Class to authenticate users
    """
    __users = []
    """A list of active users"""
    __sessions = {}
    """A nested dictionary of active sessions:
    {user_name: {session_token: timeout}}"""
    
    def __init__(self):
        """Create a new instance of the authenticator"""
        self.__users = User.select().where(True)
        
    @property
    def users(self):
        """Returns the users"""
        return self.__users
    
    @property
    def sessions(self):
        """Returns the currently active sessions"""
        return self.__sessions
    
    @property
    def active(self, user_name):
        """Determine whether a user is having an active session"""
        for user in self.sessions:
            if user == user_name:
                return True
        return False
    
    def exists(self, user_name):
        """Determines whether a user exists"""
        try:
            self.user(user_name) 
        except NoSuchUser:
            return False
        else:
            return True
    
    def user(self, user_name):
        """Try to get a user model from the database by name"""
        if user_name:
            for user in self.users:
                if user.name == user_name:
                    return user
        raise NoSuchUser(user_name)
        
    def _chkpwd(self, user_name, passwd, hashfunc=None):
        """Check a password for a user"""
        if hashfunc:
            passwd = hashfunc(passwd).hexdigest()
        if self.user(user_name).passwd == passwd:
            return True
        else:
            return False
                
    def _set_session(self, user_name, session_token_ttl):
        """Set a session token and TTL in seconds for a user"""
        self.__sessions[user_name] = session_token_ttl
        
    def _gen_session_token(self, ttl):
        """Generates a session token"""
        return {uuid4(): datetime.now() + timedelta(seconds=ttl)}
        
    def validate(self, user_name):
        """Validate a session by user name"""
        
        
    def login(self, user_name, passwd, hashfunc=None):
        """Login a user"""
        if self.active(user_name):
            raise AlreadyLoggedIn(user_name)
        else:
            if self.exists(user_name):
                
        
#===============================================================================
# Exception
#===============================================================================
class AlreadyLoggedIn(Exception):
    """Indicates that a user is already logged in"""
    pass

class NoSuchUser(Exception):
    """Indicates that a user is already logged in"""
    pass