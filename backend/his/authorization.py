"""Authorization functions."""

from typing import Iterable, Iterator, Union

from mdb import Customer

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency


__all__ = ['can_use']


Mapping = Union[AccountService, CustomerService]


def get_dependencies(service: Service) -> Iterator[Service]:
    """Returns the dependencies of a service."""

    return ServiceDependency.deps(service)


def check_dependency_tree(mapping: Mapping, service: Service) -> bool:
    """Checks the dependency tree."""

    return service in {mapping.service, *get_dependencies(mapping.service)}


def check_mappings(mappings: Iterable[Mapping], service: Service) -> bool:
    """Checks the services mappings."""

    return any(check_dependency_tree(mapping, service) for mapping in mappings)


def check_customer(customer: Union[Customer, int], service: Service) -> bool:
    """Checks the customer services."""

    return check_mappings(
        CustomerService.select(cascade=True).where(
            CustomerService.customer == customer
        ),
        service
    )


def check_account(account: Union[Account, int], service: Service) -> bool:
    """Checks the account services."""

    return check_mappings(
        AccountService.select(cascade=True).where(
            AccountService.account == account
        ),
        service
    )


def can_use(account: Account, service: Service) -> bool:
    """Checks whether the account may use the given service."""

    if account.root:
        return True

    if not check_customer(account.customer, service):
        return False

    if account.admin:
        return True

    return check_account(account, service)
