""" HIS password reset messages."""

from his.messages.api import HISMessage


__all__ = [
    'NoTokenSpecified',
    'NoPasswordSpecified',
    'PasswordResetSent',
    'PasswordResetPending',
    'InvalidResetToken',
    'PasswordSet']


class NoTokenSpecified(HISMessage):
    """Indicates that no reset token was specified."""

    STATUS = 400


class NoPasswordSpecified(HISMessage):
    """Indicates that no password was specified to set."""

    STATUS = 400


class PasswordResetSent(HISMessage):
    """Indicates that the password reset was sent."""

    STATUS = 200


class PasswordResetPending(HISMessage):
    """Indicates that a password request is already pending."""

    STATUS = 423


class InvalidResetToken(HISMessage):
    """Indicates that the request token is invalid."""

    STATUS = 401


class PasswordSet(HISMessage):
    """Indicates that the password was successfully set."""

    STATUS = 200
