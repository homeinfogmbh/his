"""Basic HIS application."""

from wsgilib import Application

from his.config import CORS, read
from his.errors import ERRORS
from his.orm import init
from his.functions import postprocess_response


__all__ = ['Application']


class Application(Application):     # pylint: disable=E0102
    """Extends wsgilib's application."""

    def __init__(self, *args, cors: dict = None, debug: bool = False,
                 **kwargs):
        """Sets default error handlers."""
        cors = CORS if cors is None else cors
        super().__init__(*args, cors=cors, debug=debug, **kwargs)
        self.before_first_request(read)
        self.after_request(postprocess_response)
        self.after_request(init)

        for exception, function in ERRORS.items():
            self.register_error_handler(exception, function)
