"""Basic HIS application."""

from flask import make_response

import wsgilib

from his.config import get_cors
from his.errors import ERRORS
from his.functions import postprocess_response


__all__ = ['Application']


class Application(wsgilib.Application):
    """HIS application base."""

    def __init__(
            self,
            *args,
            cors: callable = get_cors,
            debug: bool = False,
            **kwargs
    ):
        """Sets default error handlers."""
        super().__init__(*args, cors=cors, debug=debug, **kwargs)
        self.after_request(
            lambda response: postprocess_response(make_response(response))
        )

        for exception, function in ERRORS.items():
            self.register_error_handler(exception, function)
