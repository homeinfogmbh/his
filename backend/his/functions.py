"""Common functions."""

from his.config import COOKIE, DOMAIN


__all__ = ['set_session_cookie']


def set_session_cookie(response, session):
    """Sets the session cookie."""

    response.set_cookie(
        COOKIE, session.token.hex, expires=session.end, domain=DOMAIN,
        secure=True)
    return response
