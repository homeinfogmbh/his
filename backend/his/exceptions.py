"""Common exceptions."""

__all__ = [
    'NoSessionSpecified',
    'SessionExpired',
    'InconsistencyError',
    'ServiceExistsError',
    'AccountExistsError',
    'AmbiguousDataError',
    'PasswordResetPending'
]


class NoSessionSpecified(Exception):
    """Indicates that no session was specified."""


class SessionExpired(Exception):
    """Indicates that the respective session expired."""


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""


class AccountExistsError(Exception):
    """Indicates that the respective account already exists."""

    def __init__(self, field: str):
        super().__init__(field)
        self.field = field


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""

    def __init__(self, field: str):
        super().__init__(field)
        self.field = field

    def __str__(self):
        return self.field


class PasswordResetPending(Exception):
    """Indicates that a password reset is already pending."""
