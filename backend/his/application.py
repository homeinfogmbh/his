"""Basic HIS application."""

from itertools import chain

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidEnumerationValue
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from wsgilib import Application as _Application

from his.contextlocals import get_session
from his.messages import data
from his.messages.session import NoSessionSpecified, NoSuchSession


__all__ = ['Application']


ERROR_HANDLERS = (
    (FieldValueError, data.FieldValueError.from_fve),
    (FieldNotNullable, data.FieldNotNullable.from_fnn),
    (MissingKeyError, data.MissingKeyError.from_mke),
    (InvalidKeys, data.InvalidKeys.from_iks),
    (NonUniqueValue, data.NonUniqueValue.from_nuv),
    (InvalidEnumerationValue, data.InvalidEnumerationValue.from_iev))


def _set_session_cookie(response):
    """Sets the session cookie on the respective response."""

    print('DEBUG: Attempting to set session cookie.', flush=True)

    try:
        session = get_session()
    except NoSessionSpecified:
        print('DEBUG: No session specified.')
    except NoSuchSession:
        print('DEBUG: No such session.')
    else:
        response.set_cookie('his-session', session.token.hex)
        print('DEBUG: Set session cookie.', flush=True)

    return response


class Application(_Application):
    """Extends wsgilib's application."""

    def __init__(self, *args, debug=False, errorhandlers=None, **kwargs):
        """Sets default error handlers."""
        errorhandlers = tuple(chain(ERROR_HANDLERS, errorhandlers or ()))
        super().__init__(
            *args, cors=True, debug=debug, errorhandlers=errorhandlers,
            **kwargs)
        self.after_request(_set_session_cookie)
