"""OAuth 2.0 related models."""

from peewee import ForeignKeyField

from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from his.orm.common import HISModel
from his.orm.account import Account as User


__all__ = ['Client', 'Token', 'AuthorizationCode']


class Client(HISModel, OAuth2ClientMixin):   # pylint: disable=R0901
    """An OAuth client."""

    user = ForeignKeyField(
        User, column_name='user', backref='clients', on_delete='CASCADE')


class Token(HISModel, OAuth2TokenMixin):     # pylint: disable=R0901
    """An OAuth bearer token."""

    user = ForeignKeyField(
        User, column_name='user', backref='tokens', on_delete='CASCADE')


class AuthorizationCode(HISModel, OAuth2AuthorizationCodeMixin):
    """An OAuth authorization code."""  # pylint: disable=R0901

    user = ForeignKeyField(
        User, column_name='user', backref='authorization_codes',
        on_delete='CASCADE')


class RedirectURI(HISModel, RedirectURIMixin):
    """A redirect URI."""

    client = ForeignKeyField(
        Client, column_name='client', backref='redirect_uris',
        on_delete='CASCADE')


class GrantType(HISModel, GrantTypeMixin):
    """A grant type."""

    client = ForeignKeyField(
        Client, column_name='client', backref='grant_types',
        on_delete='CASCADE')


class ResponseType(HISModel, ResponseTypeMixin):
    """A response type."""

    
