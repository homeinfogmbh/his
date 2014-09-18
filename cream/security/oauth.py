"""
OAuth provider implementation
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

from rauth import OAuth2Service

class OAuth2Provider():
    """
    An OAuth version 2.0 service provider
    """
    name = 'CREAM'
    access_token_url = 'https://example.com/token'
    authorize_url = 'https://example.com/authorize'
    base_url = 'https://example.com/api/'
    
    @classmethod
    def authorize(cls, client):
        """
        Autorize a consumer
        """
        return OAuth2Service(name=cls.name, 
                             client_id=client.id,
                             client_secret=client.secret,
                             access_token_url=cls.access_token_url,
                             authorize_url=cls.authorize_url,
                             base_url=cls.base_url)

    @classmethod
    def __get_user_url(cls, ident):
        """
        Get the authentication URL for a consumer
        """
        return cls.base_url + '/user/' + str(ident)