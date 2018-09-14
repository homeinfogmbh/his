"""Password reset API."""

from uuid import UUID

from peeweeplus import PasswordTooShortError
from recaptcha import VerificationError, ReCaptcha

from his.config import PWRESET
from his.globals import JSON_DATA
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
        raise PasswordResetSent()   # Avoid account sniffing.


def request_reset():
    """Attempts a password reset request."""

    try:
        site_key = JSON_DATA['sitekey']
    except KeyError:
        return NoSiteKeyProvided()

    try:
        options = PWRESET[site_key]
    except KeyError:
        return SiteNotConfigured()

    secret = options['secret']
    url = options.get('url', 'https://his.homeinfo.de/pwreset.html')

    try:
        response = JSON_DATA['response']
    except KeyError:
        return NoResponseProvided()

    try:
        ReCaptcha(secret).verify(response)
    except VerificationError:
        return InvalidResponse()

    name = JSON_DATA.get('account')

    if not name:
        return NoAccountSpecified()

    account = _get_account(name)

    try:
        password_reset_token = PasswordResetToken.add(account)
    except PasswordResetPending_:
        return PasswordResetPending()

    password_reset_token.save()
    password_reset_token.email(url)
    return PasswordResetSent()


def reset_password():
    """Actually performs a password reset."""

    token = JSON_DATA.get('token')

    if not token:
        return NoTokenSpecified()

    token = UUID(token)
    passwd = JSON_DATA.get('passwd')

    if not passwd:
        return NoPasswordSpecified()

    try:
        token = PasswordResetToken.get(PasswordResetToken.token == token)
    except PasswordResetToken.DoesNotExist:
        return InvalidResetToken()

    if not token.valid:
        return InvalidResetToken()

    account = token.account

    try:
        account.passwd = passwd
    except PasswordTooShortError as password_too_short:
        return PasswordTooShort(minlen=password_too_short.minlen)

    token.delete_instance()
    account.save()
    return PasswordSet()


ROUTES = (
    ('POST', '/pwreset/request', request_reset, 'request_reset'),
    ('POST', '/pwreset/reset', reset_password, 'reset_password'))
