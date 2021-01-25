"""Authorization functions."""

from typing import Union

from peewee import ModelSelect

from mdb import Customer

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency


__all__ = ['check']


def check_dependency_tree(select: ModelSelect, service: Service) -> bool:
    """Cheks the dependency tree."""

    for mapping in select:
        if service in set(ServiceDependency.tree(mapping.service)):
            return True

    return False


def check_customer_services(customer: Union[Customer, int],
                            service: Service) -> bool:
    """Checks the customer services."""

    select = CustomerService.select().where(
        CustomerService.customer == customer)
    return check_dependency_tree(select, service)


def check_account_services(account: Union[Account, int],
                           service: Service) -> bool:
    """Checks the account services."""

    select = AccountService.select().where(AccountService.account == account)
    return check_dependency_tree(select, service)


def check(account: Union[Account, int], service: Service) -> bool:
    """Checks whether the account may use the given service."""

    if account.root:
        return True

    if not check_customer_services(account.customer, service):
        return False

    if account.admin:
        return True

    return check_account_services(account, service)
