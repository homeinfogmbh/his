"""Endpoint for reporting bugs."""

from typing import Iterator

from flask import request

from emaillib import EMail
from recaptcha import VerificationError, verify
from wsgilib import JSONMessage

from his.api import authenticated
from his.config import CONFIG, RECAPTCHA
from his.contextlocals import ACCOUNT
from his.decorators import require_json
from his.mail import MAILER


__all__ = ['ROUTES']


BUGREPORT_CONFIG = CONFIG['bugreport']


@require_json(dict)
def gen_emails() -> Iterator[EMail]:
    """Yields bug report emails."""

    template = CONFIG.get('bugreport', 'template')

    with open(template, 'r') as file:
        template = file.read()

    subject = request.json.pop('subject')
    sender = CONFIG.get('bugreport', 'sender')
    html = template.format(account=ACCOUNT, **request.json)
    recipients = CONFIG.get('bugreport', 'recipients').split()

    for recipient in recipients:
        yield EMail(subject, sender, recipient, html=html)


@authenticated
@require_json(dict)
def report() -> JSONMessage:
    """Reports a bug."""

    site_key = request.json['sitekey']

    try:
        recaptcha = RECAPTCHA[site_key]
    except KeyError:
        return JSONMessage('No ReCAPTCHA configured.', status=500)

    secret = recaptcha['secret']

    try:
        response = request.json['response']
    except KeyError:
        return JSONMessage('No ReCAPTCHA response provided.', status=400)

    try:
        verify(secret, response)
    except VerificationError:
        return JSONMessage('Invalid ReCAPTCHA response.', status=400)

    MAILER.send(gen_emails())
    return JSONMessage('Bug report submitted.', status=400)


ROUTES = [('POST', '/bugreport', report)]
