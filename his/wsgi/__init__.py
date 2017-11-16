"""HIS WSGI core services."""

from wsgilib import Router

from his.config import ROOT
from his.wsgi.account import AccountService
from his.wsgi.customer import CustomerService
from his.wsgi.service import ServicePermissions
from his.wsgi.session import SessionManager

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
ROUTER.route('/account/[id:int]')(AccountService)
ROUTER.route('/customer/[cid:int]')(CustomerService)
ROUTER.route('/service/[id:int]')(ServicePermissions)
ROUTER.route('/session/[token]')(SessionManager)
