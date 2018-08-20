"""Basic HIS application."""

from itertools import chain

from peeweeplus import FieldValueError, FieldNotNullable, MissingKeyError, \
    InvalidKeys, InvalidEnumerationValue
from wsgilib import Application as _Application

from his.messages import data

__all__ = ['Application']


ERROR_HANDLERS = (
    (FieldValueError, data.FieldValueError.from_fve),
    (FieldNotNullable, data.FieldNotNullable.from_fnn),
    (MissingKeyError, data.MissingKeyError.from_mke),
    (InvalidKeys, data.InvalidKeys.from_iks),
    (InvalidEnumerationValue, data.InvalidEnumerationValue.from_iev))


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, cors=False, debug=False, errorhandlers=None,
                 **kwargs):
        """Sets default error handlers."""
        errorhandlers = tuple(chain(ERROR_HANDLERS, errorhandlers or ()))
        super().__init__(
            *args, cors=cors, debug=debug, errorhandlers=errorhandlers,
            **kwargs)
