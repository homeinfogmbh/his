"""HIS main API."""

from functools import wraps
from typing import Callable

from his.contextlocals import SESSION, get_session_duration
from his.messages.account import ACCOUNT_LOCKED
from his.messages.account import NOT_AUTHORIZED
from his.messages.service import NO_SUCH_SERVICE
from his.messages.session import SESSION_EXPIRED
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
            raise SESSION_EXPIRED

        # Need to explicitely check SESSION.account,
        # not ACCOUNT since it might be substituted!
        if SESSION.account.unusable:
            raise ACCOUNT_LOCKED

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
            try:
                service = Service.get(Service.name == service_name)
            except Service.DoesNotExist:
                raise NO_SUCH_SERVICE from None

            if service.authorized(SESSION.account):
                return function(*args, **kwargs)

            raise NOT_AUTHORIZED

        return wrapper

    return decorator


def admin(function: Callable) -> Callable:
    """Decorator to check for administrative services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is an administrator."""
        if SESSION.account.root or SESSION.account.admin:
            return function(*args, **kwargs)

        raise NOT_AUTHORIZED

    return wrapper


def root(function: Callable) -> Callable:
    """Decorator to check for root services."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Checks whether the session's account is root."""
        if SESSION.account.root:
            return function(*args, **kwargs)

        raise NOT_AUTHORIZED

    return wrapper
