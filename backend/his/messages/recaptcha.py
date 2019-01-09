"""ReCAPTCHA related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NoResponseProvided',
    'NoSiteKeyProvided',
    'SiteNotConfigured',
    'InvalidResponse']


class NoResponseProvided(HISMessage):
    """Indicates that no ReCAPTCHA response was provided."""

    STATUS = 400


class NoSiteKeyProvided(HISMessage):
    """Indicates that no ReCAPTCHA site key was provided."""

    STATUS = 400


class SiteNotConfigured(HISMessage):
    """Indicates that no secret key is
    configured for the provided site key.
    """

    STATUS = 400


class InvalidResponse(HISMessage):
    """Indicates that the ReCAPTCHA response was invalid."""

    STATUS = 401
