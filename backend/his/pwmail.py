"""Password mailing."""

from xml.etree.ElementTree import Element, tostring

from emaillib import EMail

from his.config import CONFIG
from his.mail import get_mailer
from his.orm.pwreset import PasswordResetToken


__all__ = ['mail_password_reset_link']


def href(url: str, caption: str = None) -> str:
    """Makes a link."""

    link = Element('a', attrib={'href': url})

    if caption is not None:
        link.text = caption

    return link


def mail_password_reset_link(token: PasswordResetToken, url: str):
    """Mails the respective password reset link."""

    reply_to = CONFIG.get('pwreset', 'reply_to')
    sender = CONFIG.get('mail', 'sender')
    subject = CONFIG.get('pwreset', 'subject')
    template = CONFIG.get('pwreset', 'template')

    with open(template) as file:
        template = file.read()

    account = token.account
    link = url + '?token={}'.format(token.token.hex)
    html = template.format(account=account.name, link=tostring(href(link)))
    email = EMail(subject, sender, account.email, html=html)
    email.add_header('reply-to', reply_to)
    get_mailer().send([email])
