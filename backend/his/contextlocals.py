"""HIS request context locals."""

from flask import request
from werkzeug.local import LocalProxy

from mdb import Company, Customer

from his.config import CONFIG
from his.exceptions import InvalidData
from his.exceptions import NotAuthorized
from his.exceptions import NoSessionSpecified
from his.exceptions import SessionExpired
from his.orm.account import Account
from his.orm.session import DURATION, DURATION_RANGE, Session


__all__ = ['SESSION', 'ACCOUNT', 'CUSTOMER']


def get_session_id() -> int:
    """Returns the session ID."""

    try:
        ident = request.cookies[CONFIG.get('auth', 'session-id')]
    except KeyError:
        raise NoSessionSpecified() from None

    try:
        return int(ident)
    except ValueError:
        raise NoSessionSpecified() from None


def get_session_secret() -> str:
    """Returns the session secret."""

    try:
        return request.cookies[CONFIG.get('auth', 'session-secret')]
    except KeyError:
        raise NoSessionSpecified() from None


def get_session() -> Session:
    """Returns the session from the cache."""

    condition = Session.id == get_session_id()
    select = Session.select(Session, Account, Customer, Company)
    select = select.join(Account).join(Customer).join(Company)

    try:
        session = select.where(condition).get()
    except Session.DoesNotExist:
        raise SessionExpired() from None

    if session.verify(get_session_secret()):
        return session

    raise SessionExpired()


def get_account() -> Account:
    """Gets the verified targeted account."""

    try:
        account_id = request.args['account']
    except KeyError:
        return SESSION.account

    try:
        account_id == int(account_id)
    except (TypeError, ValueError):
        raise InvalidData(int, type(account_id)) from None

    select = Account.select(Account, Customer, Company)
    select = select.join(Customer).join(Company)
    condition = Account.id == account_id

    if SESSION.account.root:
        return select.where(condition).get()

    if SESSION.account.admin:
        condition &= Account.customer == SESSION.account.customer
        return select.where(condition).get()

    raise NotAuthorized()


def get_customer() -> Customer:
    """Gets the verified targeted customer."""

    try:
        customer_id = request.args['customer']
    except KeyError:
        return ACCOUNT.customer

    try:
        customer_id = int(customer_id)
    except (TypeError, ValueError):
        raise InvalidData(int, type(customer_id)) from None

    select = Customer.select(Customer, Company).join(Company)
    condition = Customer.id == customer_id

    if SESSION.account.root:
        return select.where(condition).get()

    raise NotAuthorized()


def get_session_duration() -> int:
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DURATION

    if duration in DURATION_RANGE:
        return duration

    return DURATION


class ModelProxy(LocalProxy):   # pylint: disable=R0903
    """Proxies ORM models."""

    def __int__(self):
        """Returns the primary key value."""
        return self.get_id()


SESSION = ModelProxy(get_session)
ACCOUNT = ModelProxy(get_account)
CUSTOMER = ModelProxy(get_customer)
