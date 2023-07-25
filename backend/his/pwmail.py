"""Password mailing."""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from xml.etree.ElementTree import Element, tostring

from emaillib import EMail

from his.config import get_config
from his.mail import get_mailer
from his.orm.pwreset import PasswordResetToken


__all__ = ["mail_password_reset_link"]


def add_token(url: str, token: str) -> str:
    """Adds a token as URL parameter."""

    scheme, netloc, path, params, query, fragment = urlparse(url)
    args = dict(parse_qsl(query))
    args.update(token=token)
    query = urlencode(args)
    return urlunparse((scheme, netloc, path, params, query, fragment))


def href(url: str, caption: str = None) -> Element:
    """Makes a link."""

    link = Element("a", attrib={"href": url})
    link.text = url if caption is None else caption
    return link


def mail_password_reset_link(token: PasswordResetToken, url: str):
    """Mails the respective password reset link."""

    reply_to = (config := get_config()).get("pwreset", "reply_to")
    sender = config.get("mail", "sender")
    subject = config.get("pwreset", "subject")
    template = config.get("pwreset", "template")

    with open(template, "r", encoding="utf-8") as file:
        template = file.read()

    url = add_token(url, token.token.hex)
    link = tostring(href(url), encoding="unicode", method="html")
    html = template.format(account=token.account.name, link=link)
    email = EMail(subject, sender, token.account.email, html=html, reply_to=reply_to)
    get_mailer().send([email])
