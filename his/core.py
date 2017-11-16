"""Core services"""

from wsgilib import Route, Router

from his.mods.account import AccountService
from his.mods.customer import CustomerService
from his.mods.service import ServicePermissions
from his.mods.session import SessionManager

__all__ = ['mk_router']


def mk_router(root):
    """Generates a router for the respective root node."""

    return Router(
        (Route('{}/account/[id:int]'.format(root)), AccountService),
        (Route('{}/customer/[cid:int]'.format(root)), CustomerService),
        (Route('{}/service/[id:int]'.format(root)), ServicePermissions),
        (Route('{}/session/[token]'.format(root)), SessionManager))
