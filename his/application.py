"""Basic HIS application."""

from peeweeplus import FieldValueError, FieldNotNullable, MissingKeyError, \
    InvalidKeys, InvalidEnumerationValue
from wsgilib import Application as _Application

from his.messages import data

__all__ = ['Application']


ERROR_HANDLERS = (
    (FieldValueError, data.FieldValueError.from_error),
    (FieldNotNullable, data.FieldNotNullable.from_error),
    (MissingKeyError, data.MissingKeyError.from_error),
    (InvalidKeys, data.InvalidKeys.from_error),
    (InvalidEnumerationValue, data.InvalidEnumerationValue.from_error))


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, cors=False, debug=False, errorhandlers=(),
                 **kwargs):
        """Sets default error handlers."""
        super().__init__(
            *args, cors=cors, debug=debug,
            errorhandlers=ERROR_HANDLERS + errorhandlers, **kwargs)
