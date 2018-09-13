"""Account management."""

from peeweeplus import PasswordTooShortError

from his.api import authenticated
from his.crypto import genpw
from his.globals import ACCOUNT, CUSTOMER, JSON_DATA
from his.messages.account import NoSuchAccount, NotAuthorized, AccountExists, \
    AccountCreated, AccountPatched, AccountsExhausted, PasswordTooShort
from his.messages.customer import CustomerUnconfigured
from his.messages.data import DataError, MissingData, InvalidData
from his.orm import AccountExistsError, AmbiguousDataError, \
    Account, CustomerSettings
from wsgilib import JSON

__all__ = ['get_account', 'ROUTES']


_USER_FIELDS = ('fullName', 'passwd', 'email')
_ADMIN_FIELDS = ('name', 'fullName', 'passwd', 'email', 'admin')


def _get_account(name_or_id):
    """Returns the respective account by its name or ID."""

    try:
        return Account.get(Account.id == int(name_or_id))
    except (ValueError, Account.DoesNotExist):
        return Account.get(Account.name == name_or_id)


def get_account(name_or_id):
    """Safely returns the respective account."""

    if ACCOUNT.root:
        try:
            return _get_account(name_or_id)
        except Account.DoesNotExist:
            raise NoSuchAccount()

    try:
        account = _get_account(name_or_id)
    except Account.DoesNotExist:
        raise NotAuthorized()   # Prevent account name sniffing.

    if ACCOUNT.admin:
        if account.customer == CUSTOMER:
            return account
    elif ACCOUNT == account:
        return account

    raise NotAuthorized()


def _add_account():
    """Adds an account for the current customer."""

    missing_fields = []
    password_generated = False

    try:
        name = JSON_DATA['name']
    except KeyError:
        missing_fields.append('name')

    try:
        email = JSON_DATA['email']
    except KeyError:
        missing_fields.append('email')

    try:
        passwd = JSON_DATA['passwd']
    except KeyError:
        passwd = genpw()
        password_generated = True

    if missing_fields:
        raise MissingData(missing_fields=missing_fields)

    try:
        account = Account.add(CUSTOMER, name, email, passwd=passwd)
    except AccountExistsError:
        raise AccountExists()
    except PasswordTooShortError as password_too_short:
        raise PasswordTooShort(minlen=password_too_short.minlen)

    account.save()

    if password_generated:
        return AccountCreated(passwd=passwd)

    return AccountCreated()


def _patch_account(account, allow=()):
    """Patches the respective account with the provided
    dictionary and an optional field restriction.
    """

    try:
        account.patch_json(JSON_DATA, allow=allow)
    except PasswordTooShortError as password_too_short:
        raise PasswordTooShort(minlen=password_too_short.minlen)
    except AmbiguousDataError as error:
        raise DataError(field=str(error))

    account.save()
    return AccountPatched()


@authenticated
def list_():
    """List one or many accounts."""

    return JSON([account.to_json() for account in ACCOUNT.subjects])


@authenticated
def get(name):
    """Gets an account by name."""

    if name == '!':
        # Return the account of the current session.
        return JSON(ACCOUNT.to_json())

    return JSON(get_account(name).to_json())


@authenticated
def add():
    """Create a new account."""

    if ACCOUNT.root:
        return _add_account()

    if ACCOUNT.admin:
        try:
            settings = CustomerSettings.get(
                CustomerSettings.customer == CUSTOMER)
        except CustomerSettings.DoesNotExist:
            return CustomerUnconfigured()

        if settings.max_accounts is None:
            return _add_account()

        accounts = sum(1 for _ in Account.select().where(
            Account.customer == CUSTOMER))

        if accounts < settings.max_accounts:
            return _add_account()

        return AccountsExhausted()

    return NotAuthorized()


@authenticated
def patch(name):
    """Modifies an account."""

    if name == '!':
        return _patch_account(ACCOUNT, allow=_USER_FIELDS)

    account = get_account(name)

    if ACCOUNT.root:
        return _patch_account(account)

    if ACCOUNT.admin and CUSTOMER == account.customer:
        return _patch_account(account, allow=_ADMIN_FIELDS)

    return NotAuthorized()


ROUTES = (
    ('GET', '/account', list_, 'list_accounts'),
    ('GET', '/account/<name>', get, 'get_account'),
    ('POST', '/account', add, 'add_account'),
    ('PATCH', '/account/<name>', patch, 'patch_account'))
