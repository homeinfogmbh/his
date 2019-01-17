"""Common functions."""

from his.config import COOKIE, DOMAIN
from his.contextlocals import get_session
from his.messages.session import NoSessionSpecified, SessionExpired


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response']


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


def postprocess_response(response):
    """Sets the session cookie on the respective response."""

    # Allow CORS credentials for AJAX.
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except (NoSessionSpecified, SessionExpired):
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
