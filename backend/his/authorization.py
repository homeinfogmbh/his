"""Authorization functions."""

from typing import Union

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency


__all__ = ['check']


def check(account: Union[Account, int], service: Service) -> bool:
    """Checks whether the account may use the given service."""

    if account.root:
        return True

    condition = AccountService.account == account
    condition &= AccountService.service == service

    for account_service in AccountService.select().where(condition):
        if service in set(ServiceDependency.tree(account_service.service)):
            break
    else:
        return False

    condition = CustomerService.customer == account.customer
    condition &= CustomerService.service == service

    for customer_service in CustomerService.active().where(condition):
        if service in set(ServiceDependency.tree(customer_service.service)):
            break
    else:
        return False

    return True
