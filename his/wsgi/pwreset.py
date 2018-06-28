"""Password reset API."""

from uuid import UUID

from peeweeplus import PasswordTooShortError
from recaptcha import ReCaptcha

from his.api import DATA
from his.config import CONFIG
from his.messages.account import NoAccountSpecified, PasswordTooShort
from his.messages.pwreset import NoTokenSpecified, NoPasswordSpecified, \
    PasswordResetSent, PasswordResetPending, InvalidResetToken, PasswordSet
from his.messages.recaptcha import NoReCaptchaResponseProvided, \
    InvalidReCaptchaResponse
from his.orm import PasswordResetPending as PasswordResetPending_, \
    Account, PasswordResetToken

__all__ = ['ROUTES']


RE_CAPTCHA = ReCaptcha(CONFIG['recaptcha']['secret'])


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
        response = json['response']
    except KeyError:
        return NoReCaptchaResponseProvided()

    if not RE_CAPTCHA.validate(response):
        return InvalidReCaptchaResponse()

    name = json.get('account')

    if not name:
        return NoAccountSpecified()

    account = _get_account(name)

    try:
        password_reset_token = PasswordResetToken.add(account)
    except PasswordResetPending_:
        return PasswordResetPending()

    password_reset_token.save()
    password_reset_token.email()
    return PasswordResetSent()


def reset_password():
    """Actually performs a password reset."""

    json = DATA.json
    token = json.get('token')

    if not token:
        return NoTokenSpecified()

    token = UUID(token)
    passwd = json.get('passwd')

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
        raise PasswordTooShort(minlen=password_too_short.minlen)

    token.delete_instance()
    account.save()
    return PasswordSet()


ROUTES = (
    ('POST', '/pwreset/request', request_reset, 'request_reset'),
    ('POST', '/pwreset/reset', reset_password, 'reset_password'))
