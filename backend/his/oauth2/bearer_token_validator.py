"""Validation of bearer tokens."""

from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2 import rfc6750

from his.orm.oauth2 import Token


__all__ = ['REQUIRE_OAUTH']


class BearerTokenValidator(rfc6750.BearerTokenValidator):
    """Validates bearer tokens."""

    def authenticate_token(self, token_string):
        """Authenticates a token."""
        try:
            return Token.get(Token.access_token == token_string)
        except Token.DoesNotExist:
            return None

    def request_invalid(self, request):
        """Determines whether the request is invalid."""
        return False

    def token_revoked(self, token):
        """Determines whether the token is revoked."""
        return token.revoked


REQUIRE_OAUTH = ResourceProtector()
REQUIRE_OAUTH.register_token_validator(BearerTokenValidator())
