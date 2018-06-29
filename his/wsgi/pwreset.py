"""Password reset API."""

from uuid import UUID

from peeweeplus import PasswordTooShortError
from recaptcha import VerificationError, ReCaptcha

from his.api import DATA
from his.config import RECAPTCHA
from his.messages.account import NoAccountSpecified, PasswordTooShort
from his.messages.pwreset import NoTokenSpecified, NoPasswordSpecified, \
    PasswordResetSent, PasswordResetPending, InvalidResetToken, PasswordSet
from his.messages.recaptcha import NoResponseProvided, NoSiteKeyProvided, \
    SiteNotConfigured, InvalidResponse
from his.orm import PasswordResetPending as PasswordResetPending_, \
    Account, PasswordResetToken

__all__ = ['ROUTES']


def _get_account(name):
    """Returns the account by its name."""

    try:
        return Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise PasswordResetSent()   # Avoid spoofing.


def request_reset():
    """Attempts a password reset request."""

    json = DATA.json

    try:
        site_key = json['sitekey']
    except KeyError:
        raise NoSiteKeyProvided()

    try:
        secret = RECAPTCHA[site_key]
    except KeyError:
        raise SiteNotConfigured()

    try:
        response = json['response']
    except KeyError:
        raise NoResponseProvided()

    try:
        ReCaptcha(secret).verify(response)
    except VerificationError:
        raise InvalidResponse()

    name = json.get('account')

    if not name:
        raise NoAccountSpecified()

    account = _get_account(name)

    try:
        password_reset_token = PasswordResetToken.add(account)
    except PasswordResetPending_:
        raise PasswordResetPending()

    password_reset_token.save()
    password_reset_token.email()
    return PasswordResetSent()


def reset_password():
    """Actually performs a password reset."""

    json = DATA.json
    token = json.get('token')

    if not token:
        raise NoTokenSpecified()

    token = UUID(token)
    passwd = json.get('passwd')

    if not passwd:
        raise NoPasswordSpecified()

    try:
        token = PasswordResetToken.get(PasswordResetToken.token == token)
    except PasswordResetToken.DoesNotExist:
        raise InvalidResetToken()

    if not token.valid:
        raise InvalidResetToken()

    account = token.account

    try:
        account.passwd = passwd
    except PasswordTooShortError as password_too_short:
        raise PasswordTooShort(minlen=password_too_short.minlen)

    token.delete_instance()
    account.save()
    return PasswordSet()


ROUTES = (
    ('POST', '/pwreset/request', request_reset, 'request_reset'),
    ('POST', '/pwreset/reset', reset_password, 'reset_password'))
