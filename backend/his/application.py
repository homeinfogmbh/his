"""Basic HIS application."""

from itertools import chain

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidEnumerationValue
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from wsgilib import Application as _Application

from his.functions import postprocess_response
from his.messages import data


__all__ = ['Application']


ERROR_HANDLERS = (
    (FieldValueError, data.FieldValueError.from_fve),
    (FieldNotNullable, data.FieldNotNullable.from_fnn),
    (MissingKeyError, data.MissingKeyError.from_mke),
    (InvalidKeys, data.InvalidKeys.from_iks),
    (NonUniqueValue, data.NonUniqueValue.from_nuv),
    (InvalidEnumerationValue, data.InvalidEnumerationValue.from_iev))


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, debug=False, errorhandlers=None, **kwargs):
        """Sets default error handlers."""
        errorhandlers = tuple(chain(ERROR_HANDLERS, errorhandlers or ()))
        super().__init__(
            *args, cors=True, debug=debug, errorhandlers=errorhandlers,
            **kwargs)
        self.after_request(postprocess_response)
