"""Handling of refresh tokens."""

from authlib.oauth2.rfc6749 import grants

from his.orm.oauth2 import Token
from his.orm.account import Account as User


__all__ = ['RefreshTokenGrant']


class RefreshTokenGrant(grants.RefreshTokenGrant):
    """Handles refresh token grants."""

    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post', 'client_secret_basic']

    def authenticate_refresh_token(self, refresh_token):
        """Authenticates the refresh token."""
        try:
            refresh_token = Token.get(refresh_token=refresh_token)
        except Token.DoesNotExist:
            return None

        if refresh_token.is_valid():
            return refresh_token

        return None

    def authenticate_user(self, credential):
        """Authenticates the user."""
        try:
            return User.get(User.user_id == credential.user_id)
        except User.DoesNotExist:
            return None

    def revoke_old_credential(self, credential):
        """Revokes the credential."""
        credential.revoked = True
        credential.save()
