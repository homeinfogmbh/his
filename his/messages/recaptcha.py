"""ReCAPTCHA related messages."""

from his.messages.api import HISMessage

__all__ = ['NoReCaptchaResponseProvided', 'InvalidReCaptchaResponse']



class NoReCaptchaResponseProvided(HISMessage):
    """Indicates that no ReCAPTCHA response was provided."""

    STATUS = 400


class InvalidReCaptchaResponse(HISMessage):
    """Indicates that the ReCAPTCHA response was invalid."""

    STATUS = 401
