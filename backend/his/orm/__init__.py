"""Object relational mappings."""

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.customer_settings import CustomerSettings
from his.orm.monkeypatches import account_active
from his.orm.monkeypatches import account_services
from his.orm.monkeypatches import service_authorized
from his.orm.pwreset import PasswordResetToken
from his.orm.service import Service, ServiceDomain
from his.orm.session import DEFAULT_SESSION_DURATION, Session


__all__ = [
    'DEFAULT_SESSION_DURATION',
    'Account',
    'AccountService',
    'CustomerService',
    'CustomerSettings',
    'PasswordResetToken',
    'Service',
    'ServiceDomain',
    'Session'
]


# Monkey patches for ORM models to aviod cyclic imports.
Account.active = property(account_active)
Account.services = property(account_services)
Service.authorized = service_authorized


MODELS = (
    Service,
    ServiceDomain,
    CustomerService,
    Account,
    AccountService,
    Session,
    CustomerSettings,
    PasswordResetToken
)
