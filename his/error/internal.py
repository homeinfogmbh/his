"""Errors for system-internal usage only"""

__all__ = ['InternalError', 'SecurityError']


# TODO: Let HTTP errors be handles by homeinfolib.wsgi.Error

class InternalError(Exception):
    """An error that is used internally only"""

    pass


class SecurityError(InternalError):
    """Indicates security violations"""

    pass
