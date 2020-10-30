"""Authorization code grants."""

from authlib.oauth2.rfc6749 import grants

from his.orm.oauth2 import AuthorizationCode
from his.orm.account import Account as User


__all__ = ['AuthorizationCodeGrant']


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    """Handles authorization code grants."""

    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post']

    def save_authorization_code(self, code, request):
        """Saves an authorization code."""
        authorization_code = AuthorizationCode(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id
        )
        authorization_code.save()

    def query_authorization_code(self, code, client):
        """Returns the authorization code."""
        try:
            return AuthorizationCode.get(
                (AuthorizationCode.code == code)
                & (AuthorizationCode.client_id == client.client_id))
        except AuthorizationCode.DoesNotExist:
            return None

    def delete_authorization_code(self, authorization_code):
        """Deletes the respective authorization code."""
        authorization_code.delete_instance()

    def authenticate_user(self, authorization_code):
        """Authenticates a user."""
        if authorization_code.user_id is None:
            return None

        try:
            return User[authorization_code.user_id]
        except User.DoesNotExist:
            return None