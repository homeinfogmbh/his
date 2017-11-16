"""HIS WSGI core services."""

from wsgilib import Router

from his.config import ROOT

__all__ = ['ROUTER']


class HISRouter(Router):
    """HIS router with variable root."""

    def __init__(self, root):
        """Sets root."""
        super().__init__()
        self.root = root

    def route(self, path):
        """Routes relative to root."""
        if path.startswith('/'):
            return super().route(self.root + path)

        return super().route(self.root + '/' + path)


ROUTER = HISRouter(ROOT)

from . import account
from . import customer
from . import service
from . import session
