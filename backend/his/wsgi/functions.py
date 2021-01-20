"""Common functions for WSGI."""

from typing import Union

from flask import request
from peewee import ModelSelect

from mdb import Company, Customer
from recaptcha import verify

from his.config import RECAPTCHA
from his.contextlocals import ACCOUNT, CUSTOMER, SESSION
from his.exceptions import NotAuthorized, RecaptchaNotConfigured
from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.customer_settings import CustomerSettings
from his.orm.service import Service
from his.orm.session import Session


__all__ = [
    'check_recaptcha',
    'get_account',
    'get_account_service',
    'get_account_services',
    'get_customer',
    'get_customer_service',
    'get_customer_services',
    'get_customer_settings',
    'get_service',
    'get_session'
]


def check_recaptcha() -> bool:
    """Checks ReCAPTCHA."""

    site_key = request.json['sitekey']

    try:
        recaptcha = RECAPTCHA[site_key]
    except KeyError:
        raise RecaptchaNotConfigured() from None

    return verify(recaptcha['secret'], request.json['response'])


def get_account(name: str) -> Account:
    """Safely returns the respective account."""

    select = Account.select(
        Account, Customer, Company).join(Customer).join(Company)

    if name == '!':
        return select.where(Account.id == ACCOUNT.id).get()

    if ACCOUNT.root:
        return select.where(Account.name == name).get()

    try:
        account = select.where(Account.name == name).get()
    except Account.DoesNotExist:
        raise NotAuthorized() from None     # Prevent account name sniffing.

    if ACCOUNT.admin and account.customer == CUSTOMER:
        return account

    if ACCOUNT.name == account.name and ACCOUNT.id == account.id:
        return account

    raise NotAuthorized()


def get_account_service(account: Union[Account, int],
                        name: str) -> AccountService:
    """Selects the account services of the give account."""

    return get_account_services(account).where(Service.name == name).get()


def get_account_services(account: Union[Account, int]) -> ModelSelect:
    """Selects the account services of the give account."""

    return AccountService.select(AccountService, Service).join(Service).where(
        AccountService.account == account)


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


def get_customer_service(customer: Union[Customer, int],
                         service: Union[Service, int]) -> CustomerService:
    """Returns the customer service mapping
    of the given customer and service.
    """

    return get_customer_services(customer).where(
        CustomerService.service == service).get()


def get_customer_services(customer: Union[Customer, int]) -> ModelSelect:
    """Selects customer service mappings for the given customer."""

    return CustomerService.select(
        CustomerService, Customer, Company, Service
    ).join(Customer).join(Company).join_from(CustomerService, Service).where(
        CustomerService.customer == customer
    )


def get_customer_settings() -> CustomerSettings:
    """Returns the respective customer settings."""

    return CustomerSettings.select().where(
        CustomerSettings.customer == CUSTOMER).get()


def get_service(name: str) -> Service:
    """Returns the respective service."""

    return Service.select().where(Service.name == name).get()


def get_session(ident: str) -> Session:
    """Returns the respective session by the
    resource identifier with authorization checks.
    """

    if ident == '!':
        return SESSION._get_current_object()    # pylint: disable=W0212

    session = Session.select(
        Session, Customer, Company).join(Customer).join(Company).where(
        Session.id == ident).get()

    if SESSION.id == session.id:
        return session

    if ACCOUNT.root:
        return session

    if ACCOUNT.admin and session.account.customer == ACCOUNT.customer:
        return session

    raise Session.DoesNotExist()
