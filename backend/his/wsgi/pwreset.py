"""Password reset API."""

from uuid import UUID

from flask import request

from wsgilib import JSONMessage, require_json

from his.config import CONFIG, RECAPTCHA
from his.orm.account import Account
from his.orm.pwreset import PasswordResetToken
from his.pwmail import mail_password_reset_link
from his.wsgi.functions import check_recaptcha


__all__ = ['ROUTES']


PASSWORD_RESET_SENT = JSONMessage('Password request sent.', status=200)

def _request_reset() -> JSONMessage:
    """Requests a reset token."""

    name = request.json.get('account')

    if not name:
        return JSONMessage('No account specified.', status=400)

    try:
        account = Account.select(cascade=True).where(
            Account.name == name).get()
    except Account.DoesNotExist:
        return PASSWORD_RESET_SENT  # Avoid account sniffing.

    token = PasswordResetToken.add(account)
    url = RECAPTCHA.get('url', CONFIG.get('pwreset', 'url'))
    mail_password_reset_link(token, url)
    return PASSWORD_RESET_SENT


@require_json(dict)
def request_reset() -> JSONMessage:
    """Attempts a password reset request."""

    if check_recaptcha():
        return _request_reset()

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

    token = PasswordResetToken.active().where(
        PasswordResetToken.token == token).get()
    token.account.passwd = passwd
    token.account.failed_logins = 0
    token.account.save()
    token.delete_instance()
    return JSONMessage('Password set.', status=200)


ROUTES = (
    ('POST', '/pwreset/request', request_reset),
    ('POST', '/pwreset/reset', reset_password)
)
