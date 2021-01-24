"""Basic HIS application."""

from wsgilib import Application

from his.config import CORS
from his.errors import ERRORS
from his.functions import postprocess_response


__all__ = ['Application']


class Application(Application):     # pylint: disable=E0102
    """Extends wsgilib's application."""

    def __init__(self, *args, cors: dict = CORS, debug: bool = False,
                 **kwargs):
        """Sets default error handlers."""
        super().__init__(*args, cors=cors, debug=debug, **kwargs)
        self.after_request(postprocess_response)

        for exception, function in ERRORS.items():
            self.register_error_handler(exception, function)
