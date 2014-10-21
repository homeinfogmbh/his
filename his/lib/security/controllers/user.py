"""
User authentication
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'

__all__ = ['UserAuthenticator', 'NoSuchUser']

from his.lib.db.models.passwd import User

class UserAuthenticator():
    """
    Class to authenticate users
    """
    __users = []
    """A list of active users"""
    
    def __init__(self):
        """Create a new instance of the authenticator"""
        self.__users = User.select().where(True)
        
    @property
    def users(self):
        """Returns the users"""
        return self.__users
    
    def user(self, user_name):
        """Try to get a user model from the database by name"""
        if user_name:
            for user in self.users:
                if user.name == user_name:
                    return user
        raise NoSuchUser(user_name)
    
    def exists(self, user_name):
        """Determines whether a user exists"""
        try:
            self.user(user_name) 
        except NoSuchUser:
            return False
        else:
            return True
        
    def chkpwd(self, user_name, passwd, hashfunc=None):
        """Check a password for a user"""
        if hashfunc:
            passwd = hashfunc(passwd).hexdigest()
        if self.user(user_name).passwd == passwd:
            return True
        else:
            return False


#===============================================================================
# Exceptions
#===============================================================================
class NoSuchUser(Exception):
    """Indicates that a user is already logged in"""
    pass