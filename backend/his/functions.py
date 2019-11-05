"""Common functions."""

from urllib.parse import urlparse

from flask import request

from his.config import COOKIE, DOMAIN
from his.contextlocals import get_session
from his.exceptions import NoSessionSpecified, SessionExpired


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


METHODS = 'GET, POST, OPTIONS, PUT, DELETE'
ALLOWED_DOMAINS = {
    'cms.homeinfo.de',
    'termgr.homeinfo.de',
    'immobit.de'
}


def set_session_cookie(response, session):
    """Sets the session cookie."""

    response.set_cookie(
        COOKIE, session.token.hex, expires=session.end, domain=DOMAIN,
        secure=True)
    return response


def delete_session_cookie(response):
    """Deletes the session cookie."""

    response.delete_cookie(COOKIE, domain=DOMAIN)
    return response


def _add_cors_headers(headers, origin):
    """Adds CORS headers."""

    headers.add('Access-Control-Allow-Origin', origin)
    headers.add('Access-Control-Allow-Credentials', 'true')
    headers.add('Access-Control-Allow-Headers', 'Content-Type')
    headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    headers.add('Access-Control-Allow-Headers', 'Authorization')
    headers.add('Access-Control-Allow-Methods', METHODS)


def _check_origin(origin):
    """Returns the HTTO referrer domain."""

    domain, *_ = urlparse(origin).netloc.split(':', maxsplit=1)

    if domain in ALLOWED_DOMAINS:
        return True

    print('CORS ERROR:', 'Referrer', domain, 'not in', ALLOWED_DOMAINS,
          flush=True)
    return False


def postprocess_response(response):
    """Sets the session cookie on the respective response."""

    # Set CORS domains.
    origin = request.headers['origin']

    if _check_origin(origin):
        _add_cors_headers(response.headers, request.referrer)

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except (NoSessionSpecified, SessionExpired):
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
