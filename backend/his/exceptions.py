"""HIS exceptions."""

__all__ = [
    'AccountLimitReached',
    'AccountLocked',
    'AmbiguousDataError',
    'AuthenticationError',
    'AuthorizationError',
    'InconsistencyError',
    'InvalidCredentials',
    'InvalidData',
    'NoSessionSpecified',
    'NotAuthorized',
    'PasswordResetPending',
    'RecaptchaNotConfigured',
    'ServiceExistsError',
    'SessionExpired',
]


class AccountLimitReached(Exception):
    """Indicates that the customer is not allowed to add more accounts."""


class AccountLocked(Exception):
    """Indicates that the account is currently locked."""


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""


class AuthenticationError(Exception):
    """Indicates an error during authentication."""


class AuthorizationError(Exception):
    """Indicates an error during authorization."""


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""


class InvalidCredentials(Exception):
    """Indicates invalid credentials such as user name or password."""


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


class RecaptchaNotConfigured(Exception):
    """Indicates that ReCAPTCHA was not configured for this site."""


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""


class SessionExpired(Exception):
    """Indicates that the respective session expired."""
