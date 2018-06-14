"""ReCAPTCHA related messages."""

from his.messages.api import Message

__all__ = [
    'NoReCaptchaResponseProvided',
    'NoSuchService',
    'ServiceAdded',
    'ServiceAlreadyEnabled',
    'AmbiguousServiceTarget',
    'MissingServiceTarget']


class _ReCaptchaMessage(Message):
    """Abstract common service message."""

    LOCALES = '/etc/his.d/locale/his/recaptcha.ini'


class NoReCaptchaResponseProvided(_ReCaptchaMessage):
    """Indicates that no ReCAPTCHA response was provided."""

    STATUS = 400


class InvalidReCaptchaResponse(_ReCaptchaMessage):
    """Indicates that the ReCAPTCHA response was invalid."""

    STATUS = 401
