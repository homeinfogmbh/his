"""HIS exceptions."""

__all__ = [
    'AccountLimitReached',
    'AccountLocked',
    'InvalidCredentials',
    'NoSessionSpecified',
    'NotAuthorized',
    'RecaptchaNotConfigured',
    'ServiceExistsError',
    'SessionExpired',
]


class AccountLimitReached(Exception):
    """Indicates that the customer is not allowed to add more accounts."""


class AccountLocked(Exception):
    """Indicates that the account is currently locked."""


class InvalidCredentials(Exception):
    """Indicates invalid credentials such as user name or password."""


class NoSessionSpecified(Exception):
    """Indicates that no session was specified."""


class NotAuthorized(Exception):
    """Indicates an error due to insufficient permissions."""


class RecaptchaNotConfigured(Exception):
    """Indicates that ReCAPTCHA was not configured for this site."""


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""


class SessionExpired(Exception):
    """Indicates that the respective session expired."""
