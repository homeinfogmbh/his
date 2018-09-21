"""HIS main API."""

from functools import wraps

from his.config import CONFIG
from his.globals import SESSION
from his.messages.account import AccountLocked
from his.messages.account import NotAuthorized
from his.messages.service import NoSuchService
from his.messages.session import NoSessionSpecified
from his.messages.session import NoSuchSession
from his.messages.session import SessionExpired
from his.orm import Service


__all__ = [
    'set_session_cookie',
    'authenticated',
    'authorized',
    'admin',
    'root']


def set_session_cookie(response, *, quiet=False):
    """Adds the session cookie to the response."""

    domain = CONFIG['auth']['domain']

    try:
        token = SESSION.token.hex
    except (NoSessionSpecified, NoSuchSession, SessionExpired):
        if not quiet:
            raise
    else:
        response.set_cookie('session', token, domain=domain)

    return response


def authenticated(function):
    """Decorator to add authentication
    checks to the respective function.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function
        with preceding authentication.
        """
        if not SESSION.alive:
            raise SessionExpired()

        if not SESSION.account.usable:
            raise AccountLocked()

        return function(*args, **kwargs)

    return wrapper


def authorized(service_name):
    """Decorator to add authorization
    checks to the respective function.
    """

    def decorator(function):
        """Wraps the respective function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function
            with preceding authorization.
            """
            try:
                service = Service.get(Service.name == service_name)
            except Service.DoesNotExist:
                raise NoSuchService()

            if service.authorized(SESSION.account):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator


def admin(function):
    """Decorator to check for administrative services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is an administrator."""
        if SESSION.account.admin:
            return function(*args, **kwargs)

        raise NotAuthorized()

    return wrapper


def root(function):
    """Decorator to check for root services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is root."""
        if SESSION.account.root:
            return function(*args, **kwargs)

        raise NotAuthorized()

    return wrapper
