"""Object relational mappings."""

from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.customer_settings import CustomerSettings
from his.orm.pwreset import PasswordResetToken
from his.orm.service import Service, ServiceDomain
from his.orm.session import ALLOWED_SESSION_DURATIONS
from his.orm.session import DEFAULT_SESSION_DURATION
from his.orm.session import Session


__all__ = [
    'ALLOWED_SESSION_DURATIONS',
    'DEFAULT_SESSION_DURATION',
    'Account',
    'AccountService',
    'CustomerService',
    'CustomerSettings',
    'PasswordResetToken',
    'Service',
    'ServiceDomain',
    'Session',
    'create_tables'
]


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


def create_tables(*args, **kwargs):
    """Creates all ORM database tables."""

    for model in MODELS:
        model.create_table(*args, **kwargs)
