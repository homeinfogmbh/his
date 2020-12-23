"""Password mailing."""

from xml.etree.ElementTree import Element, tostring

from emaillib import EMail

from his.config import CONFIG
from his.mail import MAILER, SENDER
from his.orm import PasswordResetToken


__all__ = ['mail_password_reset_link']


HREF = '<a href="{}">{}</a>'
TEMPLATE = CONFIG.get('pwreset', 'template')
SUBJECT = CONFIG.get('pwreset', 'subject')
REPLY_TO = CONFIG.get('pwreset', 'reply_to')


def href(url: str, caption: str = None) -> str:
    """Makes a link."""

    link = Element('a', attrib={'href': url})

    if caption is not None:
        link.text = caption

    return link


def mail_password_reset_link(token: PasswordResetToken, url: str):
    """Mails the respective password reset link."""

    with open(TEMPLATE) as file:
        template = file.read()

    account = token.account
    link = url + '?token={}'.format(token.token.hex)
    html = template.format(account=account.name, link=tostring(href(link)))
    email = EMail(SUBJECT, SENDER, account.email, html=html)
    email.add_header('reply-to', REPLY_TO)
    MAILER.send([email])
