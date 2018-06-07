"""Basic HIS application."""

from peeweeplus import FieldValueError, FieldNotNullable, InvalidKeys
from wsgilib import Application as _Application

from his.messages.data import InvalidData

__all__ = ['Application']


ERROR_HANDLERS = (
    (FieldNotNullable, InvalidData.from_field_not_nullable),
    (FieldValueError, InvalidData.field_value_error),
    (InvalidKeys, InvalidData.from_invalid_keys))


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, cors=False, debug=False, errorhandlers=(),
                 **kwargs):
        """Sets default error handlers."""
        super().__init__(
            *args, cors=cors, debug=debug,
            errorhandlers=ERROR_HANDLERS + errorhandlers, **kwargs)
