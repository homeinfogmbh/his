"""
Defines the HIS service template
"""
from homeinfolib.wsgi import WsgiController

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase', 'Service']


class LoginHandler(WsgiController):
    """Service that handles logins"""

    @property
    def user_name(self):
        """Returns the provided user name"""
        return self.qd.get('user_name')

    @property
    def passwd(self):
        """Returns the provided password"""
        return self.qd.get('passwd')

    def login(self):
        """Login to HIS"""
        if self.user_name:
            if self.passwd:
                try:
                    user = User.iget(User.name == )