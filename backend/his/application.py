"""Basic HIS application."""

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from wsgilib import Application as _Application

from his.config import CORS
from his.exceptions import NoSessionSpecified, SessionExpired
from his.functions import postprocess_response
from his.messages.data import field_value_error
from his.messages.data import field_not_nullable
from his.messages.data import missing_key_error
from his.messages.data import invalid_keys
from his.messages.data import non_unique_value
from his.messages.session import NO_SESSION_SPECIFIED, SESSION_EXPIRED


__all__ = ['Application']


ERROR_HANDLERS = {
    NoSessionSpecified: lambda _: NO_SESSION_SPECIFIED,
    SessionExpired: lambda _: SESSION_EXPIRED,
    FieldValueError: field_value_error,
    FieldNotNullable: field_not_nullable,
    MissingKeyError: missing_key_error,
    InvalidKeys: invalid_keys,
    NonUniqueValue: non_unique_value
}


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, cors=CORS, **kwargs):
        """Sets default error handlers."""
        super().__init__(*args, cors=cors,**kwargs)
        self.after_request(postprocess_response)

        for exception, function in ERROR_HANDLERS.items():
            self.register_error_handler(exception, function)
