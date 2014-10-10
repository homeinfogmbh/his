"""
Token management
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.10.2014'

from .models import STAClient

class ClientAuthenticator():
    """
    Simple, static client authenticator
    """
    def authenticate(self, uuid):
        """Authenticates a client by checking its UUID"""
        STAClient.select()