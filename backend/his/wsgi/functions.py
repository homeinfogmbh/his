"""Common functions for WSGI."""

from typing import Union

from peewee import ModelSelect

from mdb import Company, Customer

from his.contextlocals import ACCOUNT, CUSTOMER
from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.service import Service


__all__ = [
    'get_account_services',
    'get_account_service',
    'get_customer_services',
    'get_service'
]


def get_account_services(account: Union[Account, int]) -> ModelSelect:
    """Selects the account services of the give account."""

    return AccountService.select(AccountService, Service).join(Service).where(
        AccountService.account == account)


def get_account_service(account: Union[Account, int],
                        name: str) -> AccountService:
    """Selects the account services of the give account."""

    return get_account_services(account).where(Service.name == name).get()


def get_customer(name: str) -> Customer:
    """Returns the customer by the respective customer ID."""

    if name == '!':
        return CUSTOMER._get_current_object()   # pylint: disable=W0212

    customer = Customer.select(Customer, Company).join(Company).where(
        Customer.id == int(name)).get()

    if ACCOUNT.root or (ACCOUNT.admin and customer == ACCOUNT.customer):
        return customer

    if customer.id == CUSTOMER.id:
        return CUSTOMER._get_current_object()   # pylint: disable=W0212

    raise Customer.DoesNotExist()


def get_customer_services(customer: Union[Customer, int]) -> ModelSelect:
    """Selects customer service mappings for the given customer."""

    return CustomerService.select(
        CustomerService, Customer, Company, Service
    ).join(Customer).join(Company).join_from(CustomerService, Service).where(
        CustomerService.customer == customer
    )


def get_customer_service(customer: Union[Customer, int],
                         service: Union[Service, int]) -> CustomerService:
    """Returns the customer service mapping
    of the given customer and service.
    """

    return get_customer_services(customer).where(
        CustomerService.service == service).get()


def get_service(name: str) -> Service:
    """Returns the respective service."""

    return Service.select().where(Service.name == name).get()
