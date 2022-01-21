"""Common functions for WSGI."""

from typing import Optional

from flask import request
from peewee import Select

from mdb import Customer
from recaptcha import verify

from his.config import get_recaptcha
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
        recaptcha = get_recaptcha()[site_key]
    except KeyError:
        raise RecaptchaNotConfigured() from None

    return verify(recaptcha['secret'], request.json['response'])


def get_account(ident: Optional[int]) -> Account:
    """Safely returns the respective account."""

    if ident is None:
        return ACCOUNT._get_current_object()

    select = Account.select(cascade=True).where(Account.id == ident)

    if ACCOUNT.root:
        return select.get()

    try:
        account = select.get()
    except Account.DoesNotExist:
        raise NotAuthorized() from None     # Prevent account name sniffing.

    if ACCOUNT.admin and account.customer == CUSTOMER.id:
        return account

    if ACCOUNT.name == account.name and ACCOUNT.id == account.id:
        return account

    raise NotAuthorized()


def get_account_service(ident: int) -> AccountService:
    """Selects the account services of the give account."""

    return get_account_services().where(AccountService.id == ident).get()


def get_account_services() -> Select:
    """Selects the account services of the give account."""

    return AccountService.select(cascade=True).where(
        AccountService.account == ACCOUNT.id)


def get_customer(ident: Optional[int]) -> Customer:
    """Returns the customer by the respective customer ID."""

    if ident is None:
        return CUSTOMER._get_current_object()   # pylint: disable=W0212

    customer = Customer.select(cascade=True).where(Customer.id == ident).get()

    if ACCOUNT.root:
        return customer

    if ACCOUNT.admin and customer == ACCOUNT.customer:
        return customer

    if customer.id == CUSTOMER.id:
        return CUSTOMER._get_current_object()

    raise Customer.DoesNotExist()


def get_customer_service(ident: int) -> CustomerService:
    """Returns the customer service mapping
    of the given customer and service.
    """

    return get_customer_services().where(CustomerService.id == ident).get()


def get_customer_services() -> Select:
    """Selects customer service mappings for the given customer."""

    return CustomerService.select(cascade=True).where(
        CustomerService.customer == CUSTOMER.id)


def get_customer_settings() -> CustomerSettings:
    """Returns the respective customer settings."""

    return CustomerSettings.select().where(
        CustomerSettings.customer == CUSTOMER.id).get()


def get_service(ident: int) -> Service:
    """Returns the respective service."""

    return Service.select().where(Service.id == ident).get()


def get_session(ident: Optional[int]) -> Session:
    """Returns the respective session by the
    resource identifier with authorization checks.
    """

    if ident is None:
        return SESSION._get_current_object()

    session = Session.select(cascade=True).get()

    if SESSION.id == session.id:
        return session

    if ACCOUNT.root:
        return session

    if ACCOUNT.admin and session.account.customer == ACCOUNT.customer:
        return session

    raise Session.DoesNotExist()
