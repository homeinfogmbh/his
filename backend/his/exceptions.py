"""HIS exceptions."""

__all__ = [
    'AccountExists',
    'AmbiguousDataError',
    'AuthenticationError',
    'AuthorizationError',
    'InconsistencyError',
    'InvalidData',
    'NoSessionSpecified',
    'NotAuthorized',
    'PasswordResetPending',
    'ServiceExistsError',
    'SessionExpired',
]


class AccountExists(Exception):
    """Indicates that the respective account already exists."""


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""


class AuthenticationError(Exception):
    """Indicates an error during authentication."""


class AuthorizationError(Exception):
    """Indicates an error during authorization."""


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""


class InvalidData(Exception):
    """Indicates invalid data."""

    def __str__(self):
        """Returns an error message."""
        return 'Expected data of type "%s", but got "%s".' % self.args


class NoSessionSpecified(Exception):
    """Indicates that no session was specified."""


class NotAuthorized(Exception):
    """Indicates an error due to insufficient permissions."""


class PasswordResetPending(Exception):
    """Indicates that a password reset is already pending."""


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""


class SessionExpired(Exception):
    """Indicates that the respective session expired."""
