"""Common functions."""

from flask import Response, make_response

from his.config import get_config
from his.contextlocals import get_session_secret, get_session
from his.exceptions import NoSessionSpecified, SessionExpired
from his.orm.session import Session


__all__ = [
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


def set_session_cookie(
        response: Response, session: Session, secret: str = None
) -> Response:
    """Sets the session cookie."""

    secret = get_session_secret() if secret is None else secret

    for domain in (config := get_config()).get('auth', 'domains').split():
        response.set_cookie(
            config.get('auth', 'session-id'), str(session.id),
            expires=session.end, domain=domain, secure=True, samesite=None
        )
        response.set_cookie(
            config.get('auth', 'session-secret'), secret,
            expires=session.end, domain=domain, secure=True, samesite=None
        )

    return response


def delete_session_cookie(response: Response) -> Response:
    """Deletes the session cookie."""

    for domain in (config := get_config()).get('auth', 'domains').split():
        response.delete_cookie(config.get('auth', 'session-id'), domain=domain)
        response.delete_cookie(
            config.get('auth', 'session-secret'), domain=domain
        )

    return response


def postprocess_response(response: Response) -> Response:
    """Sets the session cookie on the respective response."""

    if not isinstance(response, Response):
        return postprocess_response(make_response(response))

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except (NoSessionSpecified, SessionExpired):
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
