"""Common exceptions."""

__all__ = [
    'InconsistencyError',
    'ServiceExistsError',
    'AccountExistsError',
    'AmbiguousDataError',
    'PasswordResetPending']


class InconsistencyError(Exception):
    """Indicates inconsistencies in database configuration."""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class ServiceExistsError(Exception):
    """Indicates that the respective account already exists."""


class AccountExistsError(Exception):
    """Indicates that the respective account already exists."""

    def __init__(self, field):
        super().__init__(field)
        self.field = field


class AmbiguousDataError(Exception):
    """Indicates that the provided data is ambiguous."""

    def __init__(self, field):
        super().__init__(field)
        self.field = field

    def __str__(self):
        return self.field


class PasswordResetPending(Exception):
    """Indicates that a password reset is already pending."""
