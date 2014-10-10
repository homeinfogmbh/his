"""
OAuth provider implementation
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '08.10.2014'

from rauth import OAuth2Service
from oauthlib.oauth2 import RequestValidator
from .models import OAuth2Client

class HISRequestValidator(RequestValidator):
    """
    HIS' request validator
    """
    def validate_client_id(self, client_id, request):
        """
        Validates a client ID
        """
        matches = [c for c in OAuth2Client.select().where(client_id=client_id)]
        if matches:
            if len(matches) == 1:
                return True
            else:
                # XXX: Ambiguous client_id is invalid
                return False
        else:
            return False
        
'''
class AuthorizationView():

    def __init__(self):
        # Using the server from previous section
        self._authorization_endpoint = server
    
    def get(self, request):
        # You need to define extract_params and make sure it does not
        # include file like objects waiting for input. In Django this
        # is request.META['wsgi.input'] and request.META['wsgi.errors']
        uri, http_method, body, headers = extract_params(request)
    
        try:
            scopes, credentials = self._authorization_endpoint.validate_authorization_request(
                uri, http_method, body, headers)
    
            # Not necessarily in session but they need to be
            # accessible in the POST view after form submit.
            request.session['oauth2_credentials'] = credentials
    
            # You probably want to render a template instead.
            response = HttpResponse()
            response.write('<h1> Authorize access to %s </h1>' % client_id)
            response.write('<form method="POST" action="/authorize">')
            for scope in scopes or []:
                response.write('<input type="checkbox" name="scopes" ' +
                'value="%s"/> %s' % (scope, scope))
                response.write('<input type="submit" value="Authorize"/>')
            return response
    
        # Errors that should be shown to the user on the provider website
        except errors.FatalClientError as e:
            return response_from_error(e)
    
        # Errors embedded in the redirect URI back to the client
        except errors.OAuth2Error as e:
            return HttpResponseRedirect(e.in_uri(e.redirect_uri))
    
    @csrf_exempt
    def post(self, request):
        uri, http_method, body, headers = extract_params(request)
    
        # The scopes the user actually authorized, i.e. checkboxes
        # that were selected.
        scopes = request.POST.getlist(['scopes'])
    
        # Extra credentials we need in the validator
        credentials = {'user': request.user}
    
        # The previously stored (in authorization GET view) credentials
        credentials.update(request.session.get('oauth2_credentials', {}))
    
        try:
            headers, body, status = self._authorization_endpoint.create_authorization_response(
            uri, http_method, body, headers, scopes, credentials)
            return response_from_return(headers, body, status)
    
        except errors.FatalClientError as e:
            return response_from_error(e)
    
    # Handles requests to /token
    class TokenView(View):
    
        def __init__(self):
            # Using the server from previous section
            self._token_endpoint = server
    
        def post(self, request):
            uri, http_method, body, headers = extract_params(request)
    
            # If you wish to include request specific extra credentials for
            # use in the validator, do so here.
            credentials = {'foo': 'bar'}
    
            headers, body, status = self._token_endpoint.create_token_response(
                    uri, http_method, body, headers, credentials)
    
            # All requests to /token will return a json response, no redirection.
            return response_from_return(headers, body, status)
    
        def response_from_return(headers, body, status):
            response = HttpResponse(content=body, status=status)
            for k, v in headers.items():
                response[k] = v
            return response
    
        def response_from_error(e)
            return HttpResponseBadRequest('Evil client is unable to send a proper request. Error is: ' + e.description)
'''


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