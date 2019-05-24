"""Password reset API."""

from uuid import UUID

from peeweeplus import PasswordTooShortError
from recaptcha import VerificationError, verify

from his.config import CONFIG, RECAPTCHA
from his.contextlocals import JSON_DATA
from his.exceptions import PasswordResetPending as PasswordResetPending_
from his.messages.account import NO_ACCOUNT_SPECIFIED, PASSWORD_TOO_SHORT
from his.messages.pwreset import INVALID_RESET_TOKEN
from his.messages.pwreset import NO_PASSWORD_SPECIFIED
from his.messages.pwreset import NO_TOKEN_SPECIFIED
from his.messages.pwreset import PASSWORD_RESET_PENDING
from his.messages.pwreset import PASSWORD_RESET_SENT
from his.messages.pwreset import PASSWORD_SET
from his.messages.recaptcha import INVALID_RESPONSE
from his.messages.recaptcha import NO_RESPONSE_PROVIDED
from his.messages.recaptcha import NO_SITE_KEY_PROVIDED
from his.messages.recaptcha import SITE_NOT_CONFIGURED
from his.orm import Account, PasswordResetToken


__all__ = ['ROUTES']


def _get_account(name):
    """Returns the account by its name."""

    try:
        return Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise PASSWORD_RESET_SENT   # Avoid account sniffing.


def request_reset():    # pylint: disable=R0911
    """Attempts a password reset request."""

    try:
        site_key = JSON_DATA['sitekey']
    except KeyError:
        return NO_SITE_KEY_PROVIDED

    try:
        recaptcha = RECAPTCHA[site_key]
    except KeyError:
        return SITE_NOT_CONFIGURED

    secret = recaptcha['secret']
    url = recaptcha.get('url', CONFIG['pwreset']['url'])

    try:
        response = JSON_DATA['response']
    except KeyError:
        return NO_RESPONSE_PROVIDED

    try:
        verify(secret, response)
    except VerificationError:
        return INVALID_RESPONSE

    name = JSON_DATA.get('account')

    if not name:
        return NO_ACCOUNT_SPECIFIED

    account = _get_account(name)

    try:
        password_reset_token = PasswordResetToken.add(account)
    except PasswordResetPending_:
        return PASSWORD_RESET_PENDING

    password_reset_token.save()
    password_reset_token.email(url)
    return PASSWORD_RESET_SENT


def reset_password():
    """Actually performs a password reset."""

    token = JSON_DATA.get('token')

    if not token:
        return NO_TOKEN_SPECIFIED

    token = UUID(token)
    passwd = JSON_DATA.get('passwd')

    if not passwd:
        return NO_PASSWORD_SPECIFIED

    try:
        token = PasswordResetToken.get(PasswordResetToken.token == token)
    except PasswordResetToken.DoesNotExist:
        return INVALID_RESET_TOKEN

    if not token.valid:
        return INVALID_RESET_TOKEN

    account = token.account

    try:
        account.passwd = passwd
    except PasswordTooShortError as password_too_short:
        return PASSWORD_TOO_SHORT.update(minlen=password_too_short.minlen)

    token.delete_instance()
    account.failed_logins = 0
    account.save()
    return PASSWORD_SET


ROUTES = (
    ('POST', '/pwreset/request', request_reset),
    ('POST', '/pwreset/reset', reset_password)
)
