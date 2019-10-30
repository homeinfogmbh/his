"""Endpoint for reporting bugs."""

from flask import request

from emaillib import EMail
from recaptcha import VerificationError, verify

from his.api import authenticated
from his.config import CONFIG, RECAPTCHA
from his.contextlocals import ACCOUNT, JSON_DATA
from his.mail import MAILER
from his.messages.bugreport import BUGREPORT_SENT
from his.messages.recaptcha import INVALID_RESPONSE
from his.messages.recaptcha import NO_RESPONSE_PROVIDED
from his.messages.recaptcha import NO_SITE_KEY_PROVIDED
from his.messages.recaptcha import SITE_NOT_CONFIGURED


__all__ = ['ROUTES']


BUGREPORT_CONFIG = CONFIG['bugreport']


def gen_emails():
    """Yields bug report emails."""

    with open(BUGREPORT_CONFIG['template'], 'r') as file:
        template = file.read()

    subject = request.json.pop('subject')
    html = template.format(account=ACCOUNT, **request.json)

    for recipient in BUGREPORT_CONFIG['recipients'].split():
        yield EMail(subject, BUGREPORT_CONFIG['sender'], recipient, html=html)


@authenticated
def report():
    """Reports a bug."""

    try:
        site_key = JSON_DATA['sitekey']
    except KeyError:
        return NO_SITE_KEY_PROVIDED

    try:
        recaptcha = RECAPTCHA[site_key]
    except KeyError:
        return SITE_NOT_CONFIGURED

    secret = recaptcha['secret']

    try:
        response = JSON_DATA['response']
    except KeyError:
        return NO_RESPONSE_PROVIDED

    try:
        verify(secret, response)
    except VerificationError:
        return INVALID_RESPONSE

    emails = tuple(gen_emails())
    MAILER.send(emails)
    return BUGREPORT_SENT


ROUTES = (('POST', '/bugreport', report),)
