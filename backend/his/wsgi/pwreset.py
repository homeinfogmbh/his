"""Password reset API."""

from uuid import UUID

from flask import request

from recaptcha import verify
from wsgilib import JSONMessage

from his.config import CONFIG, RECAPTCHA
from his.decorators import require_json
from his.errors import INVALID_RESET_TOKEN
from his.exceptions import PasswordResetPending, RecaptchaNotConfigured
from his.orm.account import Account
from his.orm.pwreset import PasswordResetToken
from his.pwmail import mail_password_reset_link


__all__ = ['ROUTES']


PASSWORD_RESET_SENT = JSONMessage('Password request sent.', status=200)


@require_json(dict)
def request_reset():    # pylint: disable=R0911
    """Attempts a password reset request."""

    site_key = request.json['sitekey']

    try:
        recaptcha = RECAPTCHA[site_key]
    except KeyError:
        raise RecaptchaNotConfigured() from None

    verify(recaptcha['secret'], request.json['response'])
    name = request.json.get('account')

    if not name:
        return JSONMessage('No account specified.', status=400)

    try:
        account = Account.get(Account.name == name)
    except Account.DoesNotExist:
        return PASSWORD_RESET_SENT  # Avoid account sniffing.

    try:
        password_reset_token = PasswordResetToken.add(account)
    except PasswordResetPending:
        return JSONMessage('Password request pending.', status=200)

    password_reset_token.save()
    url = recaptcha.get('url', CONFIG.get('pwreset', 'url'))
    mail_password_reset_link(password_reset_token.email, url)
    return PASSWORD_RESET_SENT


@require_json(dict)
def reset_password() -> JSONMessage:
    """Actually performs a password reset."""

    token = request.json.get('token')

    if not token:
        return JSONMessage('No token specified.', status=400)

    token = UUID(token)
    passwd = request.json.get('passwd')

    if not passwd:
        return JSONMessage('No password specified.', status=400)

    token = PasswordResetToken.select(
        PasswordResetToken, Account).join(Account).where(
        PasswordResetToken.token == token).get()

    if not token.valid:
        return INVALID_RESET_TOKEN

    token.delete_instance()
    token.account.passwd = passwd
    token.account.failed_logins = 0
    token.account.save()
    return JSONMessage('Password set.', status=200)


ROUTES = (
    ('POST', '/pwreset/request', request_reset),
    ('POST', '/pwreset/reset', reset_password)
)
