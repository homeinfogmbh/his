"""Decorators for WSGI functions."""

from functools import wraps
from typing import Any, Callable, Optional

from flask import request

from his.exceptions import InvalidData
from his.wsgi.functions import get_session


__all__ = ['require_json', 'with_session']


AnyFunc = Callable[..., Any]


def require_json(typ: type) -> Callable[[AnyFunc], AnyFunc]:
    """Checks for valid JSON data."""

    def decorator(function: AnyFunc) -> AnyFunc:
        """Decorates the function."""
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            """Wraps the original function."""
            if isinstance(request.json, typ):
                return function(*args, **kwargs)

            raise InvalidData(typ, type(request.json))

        return wrapper

    return decorator


def with_session(function: AnyFunc) -> AnyFunc:
    """Converts the first argument of function into a sesion."""

    @wraps(function)
    def wrapper(ident: Optional[int], *args, **kwargs) -> Any:
        return function(get_session(ident), *args, **kwargs)

    return wrapper
