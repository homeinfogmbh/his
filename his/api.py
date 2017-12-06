"""HIS main API."""

from peewee import DoesNotExist
from wsgilib import PostData

from his.globals import SESSION
from his.messages.account import NotAuthorized
from his.messages.data import NoDataProvided, InvalidUTF8Data, InvalidJSON
from his.messages.service import NoSuchService
from his.messages.session import SessionExpired
from his.orm import Service

__all__ = ['DATA', 'authenticated', 'authorized', 'admin', 'root']


DATA = PostData(
    no_data_provided=NoDataProvided(),
    non_utf8_data=InvalidUTF8Data(),
    non_json_data=InvalidJSON())


def authenticated(function):
    """Decorator to add authentication
    checks to the respective function.
    """

    def authentication_wrapper(*args, **kwargs):
        """Wraps the respective function
        with preceding authentication.
        """
        if SESSION.active:
            return function(*args, **kwargs)

        raise SessionExpired()

    return authentication_wrapper


def authorized(service_name):
    """Decorator to add authorization
    checks to the respective function.
    """

    def authorized_decorator(function):
        """Wraps the respective function."""

        def authorized_wrapper(*args, **kwargs):
            """Wraps the respective function
            with preceding authentication.
            """
            try:
                service = Service.get(Service.name == service_name)
            except DoesNotExist:
                raise NoSuchService()

            if service.authorized(SESSION.account):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return authorized_wrapper

    return authorized_decorator


def admin(function):
    """Decorator to check for administrative services."""

    def admin_wrapper(*args, **kwargs):
        """Checks whether the session's account is an administrator."""
        if SESSION.account.admin:
            return function(*args, **kwargs)

        raise NotAuthorized() from None

    return admin_wrapper


def root(function):
    """Decorator to check for root services."""

    def root_wrapper(*args, **kwargs):
        """Checks whether the session's account is root."""
        if SESSION.account.root:
            return function(*args, **kwargs)

        raise NotAuthorized() from None

    return root_wrapper
