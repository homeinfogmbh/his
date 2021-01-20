"""HIS exceptions."""

__all__ = [
    'AccountExistsError',
    'AmbiguousDataError',
    'AuthenticationError',
    'AuthorizationError',
    'InconsistencyError',
    'NoSessionSpecified',
    'NotAuthorized',
    'PasswordResetPending',
    'ServiceExistsError',
    'SessionExpired',
]


class AccountExistsError(Exception):
    """Indicates that the respective account already exists."""


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""


class AuthenticationError(Exception):
    """Indicates an error during authentication."""


class AuthorizationError(Exception):
    """Indicates an error during authorization."""


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""


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
