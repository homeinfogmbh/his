"""Common functions."""

from his.config import DOMAINS, SESSION_ID, SESSION_SECRET
from his.contextlocals import get_session_secret, get_session
from his.exceptions import NoSessionSpecified, SessionExpired


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


def set_session_cookie(response, session, secret=None):
    """Sets the session cookie."""

    secret = get_session_secret() if secret is None else secret

    for domain in DOMAINS:
        response.set_cookie(
            SESSION_ID, str(session.id), expires=session.end, domain=domain,
            secure=True)
        response.set_cookie(
            SESSION_SECRET, secret, expires=session.end, domain=domain,
            secure=True)

    return response


def delete_session_cookie(response):
    """Deletes the session cookie."""

    for domain in DOMAINS:
        response.delete_cookie(SESSION_ID, domain=domain)
        response.delete_cookie(SESSION_SECRET, domain=domain)

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
