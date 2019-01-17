"""HIS main API."""

from functools import wraps

from functoolsplus import coerce

from his.contextlocals import SESSION
from his.messages.account import AccountLocked
from his.messages.account import NotAuthorized
from his.messages.service import NoSuchService
from his.messages.session import SessionExpired
from his.orm import Service


__all__ = [
    'domains',
    'authenticated',
    'authorized',
    'admin',
    'root']


@coerce(frozenset)
def domains():
    """Returns a list of domains for the cookie."""

    for service in Service:
        for domain in service.domains:
            yield domain.domain


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
        if SESSION.account.root or SESSION.account.admin:
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
