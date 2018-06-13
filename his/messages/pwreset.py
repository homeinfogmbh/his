""" HIS password reset messages."""

from his.messages.common import Message

__all__ = [
    'NoTokenSpecified',
    'NoPasswordSpecified',
    'PasswordResetSent',
    'PasswordResetPending',
    'InvalidResetToken',
    'PasswordSet']


class _PwResetMessage(Message):
    """Abstract common password reset message."""

    LOCALES = '/etc/his.d/locale/his/pwreset.ini'


class NoTokenSpecified(_PwResetMessage):
    """Indicates that no reset token was specified."""

    STATUS = 400


class NoPasswordSpecified(_PwResetMessage):
    """Indicates that no password was specified to set."""

    STATUS = 400


class PasswordResetSent(_PwResetMessage):
    """Indicates that the password reset was sent."""

    STATUS = 200


class PasswordResetPending(_PwResetMessage):
    """Indicates that a password request is already pending."""

    STATUS = 423


class InvalidResetToken(_PwResetMessage):
    """Indicates that the request token is invalid."""

    STATUS = 401


class PasswordSet(_PwResetMessage):
    """Indicates that the password was successfully set."""

    STATUS = 200
