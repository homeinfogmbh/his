"""Monkey patches for ORM models to aviod cyclic imports."""

from his.messages.service import SERVICE_LOCKED
from his.orm.customer_service import CustomerService
from his.orm.proxy import AccountServicesProxy
from his.orm.session import Session


__all__ = ['account_active', 'account_services', 'service_authorized']


def account_active(self):
    """Determines whether the account has an open session."""

    for session in Session.select().where(Session.account == self):
        if session.alive:
            return True

    return False


def account_services(self):
    """Returns an account <> service mapping proxy."""

    return AccountServicesProxy(self)


def service_authorized(self, account):
    """Determines whether the respective account
    is authorized to use this service.

    An account is considered authorized if:
        1) account is root or
        2) account's customer is enabled for the service and
            2a) account is admin or
            2b) account is enabled for the service
    """

    if account.root:
        return True

    if self.locked:
        raise SERVICE_LOCKED

    if self in CustomerService.services(account.customer):
        return account.admin or self in account.services

    return False
