"""
OAuth provider implementation
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '08.10.2014'
__credits__ = 'To the oauthlib documentation at <https://oauthlib.readthedocs.org>'

from .abc import OAuth2Model
from peewee import TextField, ForeignKeyField, DateTimeField

class User(OAuth2Model):
    """
    The user of your site which resources might be access by clients upon \
    authorization from the user. In our example we will re-use the User model \
    provided in django.contrib.auth.models. How the user authenticates is \
    orthogonal from OAuth and may be any way you prefer
    """
    pass


class Client(OAuth2Model):
    """
    The client interested in accessing protected resources.
    """
    cid = TextField()
    """Required. 
    The identifier the client will use during the OAuth workflow. 
    Structure is up to you and may be a simple UUID."""
    user = ForeignKeyField(User, related_name='client')
    """Recommended. 
    It is common practice to link each client with one of your existing users. 
    Whether you do associate clients and users or not, ensure you are able \
    to protect yourself against malicious clients."""
    grant_type = TextField()
    """Required. 
    The grant type the client may utilize. 
    This should only be one per client as each grant type has different \
    security properties and it is best to keep them separate to avoid \
    mistakes."""
    response_type = TextField()
    """Required, if using a grant type with an associated response type \
    (eg. Authorization Code Grant) or using a grant which only utilizes \
    response types (eg. Implicit Grant)."""
    scopes = TextField()
    """Required. 
    The list of scopes the client may request access to.
    If you allow multiple types of grants this will vary related to their \
    different security properties. 
    For example, the Implicit Grant might only allow read-only scopes but \
    the Authorization Grant also allow writes."""
    redirect_uris = TextField()
    """These are the absolute URIs that a client may use to redirect to \
    after authorization. 
    You should never allow a client to redirect to a URI that has not \
    previously been registered."""
    
    
class BearerToken(OAuth2Model):
    """
    The most common type of OAuth 2 token. Through the documentation this \
    will be considered an object with several properties, such as token type \
    and expiration date, and distinct from the access token it contains.
    Think of OAuth 2 tokens as containers and access tokens and refresh \
    tokens as text.
    """
    client = ForeignKeyField(Client, related_name='bearer_token')
    """Association with the client to whom the token was given."""
    user = ForeignKeyField(User, related_name='bearer_token')
    """Association with the user to which protected \
    resources this token grants access."""
    scopes = TextField()
    """Scopes to which the token is bound. Attempt to access protected \
    resources outside these scopes will be denied."""
    access_token = TextField()
    """An unguessable unique string of characters."""
    refresh_token = TextField()
    """An unguessable unique string of characters. 
    This token is only supplied to confidential clients. 
    For example the Authorization Code Grant or the Resource Owner \
    Password Credentials Grant."""
    expires_at = DateTimeField()
    """Exact time of expiration. Commonly this is one hour after creation."""
        
        
class AuthorizationCode(OAuth2Model):
    """
    This is specific to the Authorization Code grant and represent the \
    temporary credential granted to the client upon successful authorization. \
    It will later be exchanged for an access token, when that is done it \
    should cease to exist. 
    It should have a limited life time, less than ten minutes. 
    This model is similar to the Bearer Token as it mainly acts a temporary \
    storage of properties to later be transferred to the token.
    """
    client = ForeignKeyField(Client, related_name='authorization_code')
    """Association with the client to whom the token was given."""
    user = ForeignKeyField(User, related_name='authorization_code')
    """Association with the user to which protected \
    resources this token grants access."""
    scopes = TextField()
    """Scopes to which the token is bound. 
    Attempt to access protected resources outside these scopes \
    will be denied."""
    code = TextField()
    """An unguessable unique string of characters."""
    expires_at = DateTimeField()
    """Exact time of expiration. 
    Commonly this is under ten minutes after creation."""
    

class OAuth2Service(OAuth2Model):
    """
    Describes an OAuth-protected web-service
    """
    name = TextField()
    """"A unique name"""
    base_url = TextField()
    """The OAuth 2.0 Base URL"""
    authorize_url = TextField()
    """The OAuth 2.0 Authorize URL"""
    access_token_url = TextField()
    """The OAuth 2.0 Access Token URL"""