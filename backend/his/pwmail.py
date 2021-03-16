"""Password mailing."""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from xml.etree.ElementTree import Element, tostring

from emaillib import EMail

from his.config import CONFIG
from his.mail import get_mailer
from his.orm.pwreset import PasswordResetToken


__all__ = ['mail_password_reset_link']


def add_token(url: str, token: str) -> str:
    """Adds a token as URL parameter."""

    scheme, netloc, path, params, query, fragment = urlparse(url)
    args = dict(parse_qsl(query))
    args.update(token=token)
    query = urlencode(args)
    return urlunparse((scheme, netloc, path, params, query, fragment))


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

    link = tostring(href(add_token(url, token.token.hex)))
    html = template.format(account=token.account.name, link=link)
    email = EMail(subject, sender, token.account.email, html=html)
    email.add_header('reply-to', reply_to)
    get_mailer().send([email])
