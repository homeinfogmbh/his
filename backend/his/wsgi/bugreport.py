"""Endpoint for reporting bugs."""

from typing import Iterator

from flask import request

from emaillib import EMail
from wsgilib import JSONMessage, require_json

from his.api import authenticated
from his.config import get_config
from his.contextlocals import ACCOUNT
from his.mail import get_mailer
from his.wsgi.functions import check_recaptcha


__all__ = ['ROUTES']


@require_json(dict)
def gen_emails() -> Iterator[EMail]:
    """Yields bug report emails."""

    sender = (config := get_config()).get('bugreport', 'sender')
    recipients = config.get('bugreport', 'recipients').split()
    template = config.get('bugreport', 'template')

    with open(template, 'r', encoding='utf-8') as file:
        template = file.read()

    subject = request.json.pop('subject')
    html = template.format(account=ACCOUNT, **request.json)

    for recipient in recipients:
        yield EMail(subject, sender, recipient, html=html)


@authenticated
@require_json(dict)
def report() -> JSONMessage:
    """Reports a bug."""

    if check_recaptcha():
        get_mailer().send(gen_emails())

    return JSONMessage('Bug report submitted.', status=200)


ROUTES = [('POST', '/bugreport', report)]
