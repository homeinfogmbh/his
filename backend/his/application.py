"""Basic HIS application."""

from functools import partial
from itertools import chain

from peeweeplus import FieldValueError, FieldNotNullable, MissingKeyError, \
    InvalidKeys, NonUniqueValue, InvalidEnumerationValue
from wsgilib import Application as _Application

from his.messages import data
from his.api import set_session_cookie


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

    def __init__(self, *args, cors=False, debug=False, errorhandlers=None,
                 **kwargs):
        """Sets default error handlers."""
        errorhandlers = tuple(chain(ERROR_HANDLERS, errorhandlers or ()))
        super().__init__(
            *args, cors=cors, debug=debug, errorhandlers=errorhandlers,
            **kwargs)
        self.after_request(partial(set_session_cookie, quiet=True))
