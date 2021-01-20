"""Authorization functions."""

from typing import Union

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.service import Service


__all__ = ['check']


def check(account: Union[Account, int], service: Service) -> bool:
    """Checks whether the account may use the given service."""

    condition = AccountService.account == account
    condition &= AccountService.service == service

    for account_service in AccountService.select().where(condition):
        if service in account_service.service.dependencies:
            break
    else:
        return False

    condition = CustomerService.customer == account.customer
    condition &= CustomerService.service == service

    for customer_service in CustomerService.active().where(condition):
        if service in customer_service.service.dependencies:
            break
    else:
        return False

    return True
