"""HIS main API."""

from functools import wraps

from wsgilib import PostData

from his.globals import SESSION
from his.messages import NotAuthorized, AccountLocked, NoDataProvided, \
    InvalidUTF8Data, InvalidJSON, NoSuchService, SessionExpired
from his.orm import Service

__all__ = ['DATA', 'authenticated', 'authorized', 'admin', 'root']


DATA = PostData(
    no_data_provided=NoDataProvided,
    non_utf8_data=InvalidUTF8Data,
    non_json_data=InvalidJSON)


def authenticated(function):
    """Decorator to add authentication
    checks to the respective function.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function
        with preceding authentication.
        """
        if SESSION.account.usable:
            if SESSION.alive:
                return function(*args, **kwargs)

            raise SessionExpired()

        raise AccountLocked()

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
