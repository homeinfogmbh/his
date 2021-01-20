"""HIS main API."""

from functools import wraps
from typing import Callable

from his.contextlocals import SESSION, get_session_duration
from his.exceptions import AccountLocked, NotAuthorized, SessionExpired
from his.orm import Service


__all__ = ['authenticated', 'authorized', 'admin', 'root']


def authenticated(function: Callable) -> Callable:
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

        # Need to explicitely check SESSION.account,
        # not ACCOUNT since it might be substituted!
        if SESSION.account.unusable:
            raise AccountLocked()

        SESSION.renew(duration=get_session_duration())
        return function(*args, **kwargs)

    return wrapper


def authorized(service_name: str) -> Callable:
    """Decorator to add authorization
    checks to the respective function.
    """

    def decorator(function: Callable) -> Callable:
        """Wraps the respective function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function
            with preceding authorization.
            """
            service = Service.get(Service.name == service_name)

            if service.authorized(SESSION.account):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator


def admin(function: Callable) -> Callable:
    """Decorator to check for administrative services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is an administrator."""
        if SESSION.account.root or SESSION.account.admin:
            return function(*args, **kwargs)

        raise NotAuthorized()

    return wrapper


def root(function: Callable) -> Callable:
    """Decorator to check for root services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is root."""
        if SESSION.account.root:
            return function(*args, **kwargs)

        raise NotAuthorized()

    return wrapper
