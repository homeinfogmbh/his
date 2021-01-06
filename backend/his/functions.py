"""Common functions."""

from flask import Response
from werkzeug.http import dump_cookie

from his.config import DOMAINS, SESSION_ID, SESSION_SECRET
from his.contextlocals import get_session_secret, get_session
from his.exceptions import NoSessionSpecified, SessionExpired
from his.orm import Session


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


def set_cookie(response: Response, *args, **kwargs):
    """A workaround for explicitly setting SameSite to None
    Until the following fix is released:
    https://github.com/pallets/werkzeug/issues/1549
    """

    cookie = dump_cookie(*args, **kwargs)

    if 'samesite' in kwargs and kwargs['samesite'] is None:
        cookie = f'{cookie}; SameSite=None'

    response.headers.add('Set-Cookie', cookie)


def set_session_cookie(response: Response, session: Session,
                       secret: str = None) -> Response:
    """Sets the session cookie."""

    secret = get_session_secret() if secret is None else secret

    for domain in DOMAINS:
        set_cookie(
            response, SESSION_ID, str(session.id), expires=session.end,
            domain=domain, secure=True, samesite=None)
        set_cookie(
            response, SESSION_SECRET, secret, expires=session.end,
            domain=domain, secure=True, samesite=None)

    return response


def delete_session_cookie(response: Response) -> Response:
    """Deletes the session cookie."""

    for domain in DOMAINS:
        response.delete_cookie(SESSION_ID, domain=domain)
        response.delete_cookie(SESSION_SECRET, domain=domain)

    return response


def postprocess_response(response: Response) -> Response:
    """Sets the session cookie on the respective response."""

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except (NoSessionSpecified, SessionExpired):
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
