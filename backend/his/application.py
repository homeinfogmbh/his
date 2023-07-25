"""Basic HIS application."""

import wsgilib

from his.config import get_cors
from his.errors import ERRORS
from his.session import postprocess_response


__all__ = ["Application"]


class Application(wsgilib.Application):
    """HIS application base."""

    def __init__(self, *args, cors: callable = get_cors, debug: bool = False, **kwargs):
        """Sets default error handlers."""
        super().__init__(*args, cors=cors, debug=debug, **kwargs)
        self.after_request(postprocess_response)

        for exception, function in ERRORS.items():
            self.register_error_handler(exception, function)
