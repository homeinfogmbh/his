"""Toaken revication endpoint."""

from authlib.oauth2.rfc7009 import RevocationEndpoint

from comcatlib.orm.oauth import Token


__all__ = ['TokenRevocationEndpoint']


class TokenRevocationEndpoint(RevocationEndpoint):
    """A Token revocation endpoint."""

    def query_token(self, token, token_type_hint, client):
        """Queries a token from the database."""
        match_client = Token.client_id == client.client_id
        access_token = Token.access_token == token
        refresh_token = Token.refresh_token == token

        if token_type_hint == 'access_token':
            select = match_client & access_token
        elif token_type_hint == 'refresh_token':
            select = match_client & refresh_token
        else:   # without token_type_hint
            select = match_client & (access_token | refresh_token)

        try:
            return Token.get(select)
        except Token.DoesNotExist:
            return None

    def revoke_token(self, token):
        """Revokes the respective token."""
        token.revoked = True
        token.save()
