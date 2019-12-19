"""Common functions."""

from his.config import COOKIE, DOMAINS
from his.contextlocals import get_session_token, get_session
from his.exceptions import NoSessionSpecified, SessionExpired


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


def set_session_cookie(response, session, token=None):
    """Sets the session cookie."""

    token = get_session_token() if token is None else token

    for domain in DOMAINS:
        response.set_cookie(
            COOKIE, token, expires=session.end, domain=domain, secure=True)

    return response


def delete_session_cookie(response):
    """Deletes the session cookie."""

    for domain in DOMAINS:
        response.delete_cookie(COOKIE, domain=domain)

    return response


def postprocess_response(response):
    """Sets the session cookie on the respective response."""

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except (NoSessionSpecified, SessionExpired):
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
