"""Miscellaneous functions."""

from typing import Iterable, Union

from his.orm import Account, AccountService, CustomerService, Service


__all__ = ["stakeholders"]


def stakeholders(service: Union[Service, str]) -> Iterable[Account]:
    """Select accounts that can use the given service."""

    if isinstance(service, str):
        service = Service.get(Service.name == service)

    return (
        Account.select()
        .join(AccountService)
        .join_from(
            Account, CustomerService, on=Account.customer == CustomerService.customer
        )
        .where(
            (AccountService.service == service) & (CustomerService.service == service)
        )
    )
