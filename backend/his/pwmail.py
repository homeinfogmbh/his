"""Password mailing."""

from emaillib import EMail

from his.config import CONFIG
from his.mail import MAIL_CFG, MAILER


__all__ = ['mail_password_reset_link']


HREF = '<a href="{}">{}</a>'
PWRESET_CFG = CONFIG['pwreset']


def href(url, caption=None):
    """Makes a link."""

    if caption is None:
        caption = url

    return HREF.format(url, caption)


def mail_password_reset_link(password_reset_token, url):
    """Mails the respective password reset link."""

    with open(PWRESET_CFG['template']) as file:
        template = file.read()

    account = password_reset_token.account
    link = url + '?token={}'.format(password_reset_token.token.hex)
    html = template.format(account=account.name, link=href(link))
    email = EMail(
        PWRESET_CFG['subject'], MAIL_CFG['sender'], account.email,
        html=html)
    email.add_header('reply-to', PWRESET_CFG['reply_to'])
    MAILER.send([email])
    return True
