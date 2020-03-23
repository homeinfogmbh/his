"""Token introspection endpoint."""

from authlib.oauth2.rfc7662 import IntrospectionEndpoint

from his.orm.oauth2 import Token


__all__ = ['TokenIntrospectionEndpoint']


URL = 'https://comcat.homeinfo.de/'


def get_token(token, token_type_hint):  # pylint: disable=R0911
    """Returns the respective token."""

    if token_type_hint == 'access_token':
        return Token.get(Token.access_token == token)

    if token_type_hint == 'refresh_token':
        return Token.get(Token.refresh_token == token)

    try:
        return Token.get(Token.access_token == token)
    except Token.DoesNotExist:
        return Token.get(Token.refresh_token == token)


class TokenIntrospectionEndpoint(IntrospectionEndpoint):
    """Introspection of bearer tokens."""

    def query_token(self, token, token_type_hint, client):
        """Returns the respective token."""
        try:
            token = get_token(token, token_type_hint)
        except Token.DoesNotExist:
            return None

        if token.client_id == client.client_id:
            return token

        return None

    def introspect_token(self, token):
        """Returns a JSON-ish dict of the token."""
        return {
            'active': True,
            'client_id': token.client_id,
            'token_type': token.token_type,
            'username': token.user.uuid.hex,
            'scope': token.get_scope(),
            'sub': token.user.uuid.hex,
            'aud': token.client_id,
            'iss': URL,
            'exp': token.expires_at,
            'iat': token.issued_at,
        }
