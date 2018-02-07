"""Account management."""

from his.api import DATA, authenticated
from his.crypto import genpw
from his.globals import ACCOUNT, CUSTOMER
from his.messages.account import NoSuchAccount, NotAuthorized, AccountExists, \
    AccountCreated, AccountPatched, AccountsExhausted
from his.messages.customer import CustomerUnconfigured
from his.messages.data import DataError, MissingData, InvalidData
from his.orm import AccountExists as AccountExists_, AmbiguousDataError, \
    Account, CustomerSettings
from wsgilib import JSON

__all__ = ['ROUTES']


def account_by_name(name_or_id):
    """Returns the respective account by its name."""

    try:
        ident = int(name_or_id)
    except ValueError:
        try:
            return Account.get(Account.name == name_or_id)
        except Account.DoesNotExist:
            raise NoSuchAccount()

    try:
        return Account.get(Account.id == ident)
    except Account.DoesNotExist:
        raise NoSuchAccount()


def add_account():
    """Adds an account for the current customer."""

    json = DATA.json
    missing_fields = []
    password_generated = False

    try:
        name = json['name']
    except KeyError:
        missing_fields.append('name')

    try:
        email = json['email']
    except KeyError:
        missing_fields.append('email')

    try:
        passwd = json['passwd']
    except KeyError:
        passwd = genpw()
        password_generated = True

    if missing_fields:
        raise MissingData(missing_fields=missing_fields)

    try:
        account = Account.add(CUSTOMER, name, email, passwd=passwd)
    except AccountExists_:
        raise AccountExists()

    account.save()

    if password_generated:
        return AccountCreated(passwd=passwd)

    return AccountCreated()


def patch_root(account):
    """Patches the account from a root user context."""

    try:
        account.patch(DATA.json)
        account.save()
    except (TypeError, ValueError):
        raise InvalidData()
    except AmbiguousDataError as error:
        raise DataError(field=str(error))

    return AccountPatched()


def patch_admin(account):
    """Patches the account from an admin context."""

    patch_dict = {}
    invalid_keys = []

    # Filter valid options for admins.
    for key, value in DATA.json.items():
        if key in ('name', 'passwd', 'email', 'admin'):
            patch_dict[key] = value
        else:
            invalid_keys.append(key)

    try:
        account.patch(patch_dict)
        account.save()
    except (TypeError, ValueError):
        raise InvalidData()
    except AmbiguousDataError as error:
        raise DataError(field=str(error))

    return AccountPatched(invalid_keys=invalid_keys)


def patch_user(account):
    """Patches the accunt from a user context."""

    patch_dict = {}
    invalid_keys = []

    # Filter valid options for normal users.
    for key, value in DATA.json.items():
        if key in ('passwd', 'email'):
            patch_dict[key] = value
        else:
            invalid_keys.append(key)

    try:
        account.patch(patch_dict)
        account.save()
    except (TypeError, ValueError):
        raise InvalidData()
    except AmbiguousDataError as error:
        raise DataError(field=str(error))

    if invalid_keys:
        return AccountPatched(invalid_keys=invalid_keys)

    return AccountPatched()


@authenticated
def list_():
    """List one or many accounts."""

    return JSON([account.to_dict() for account in account.subjects])


@authenticated
def get(name):
    """Gets an account by name."""

    if name == '!':
        # Return the account of the current session.
        return JSON(ACCOUNT.to_dict())

    account = account_by_name(name)

    if ACCOUNT.root:
        return JSON(account.to_dict())
    elif ACCOUNT.admin:
        if account.customer == CUSTOMER:
            return JSON(account.to_dict())

        raise NotAuthorized()
    elif ACCOUNT == account:
        return JSON(account.to_dict())

    raise NotAuthorized()


@authenticated
def add():
    """Create a new account."""

    if ACCOUNT.root:
        return add_account()
    elif ACCOUNT.admin:
        try:
            settings = CustomerSettings.get(
                CustomerSettings.customer == CUSTOMER)
        except CustomerSettings.DoesNotExist:
            raise CustomerUnconfigured()

        if settings.max_accounts is None:
            return add_account()

        accounts = sum(1 for _ in Account.select().where(
            Account.customer == CUSTOMER))

        if accounts < settings.max_accounts:
            return add_account()

        raise AccountsExhausted()

    raise NotAuthorized()


@authenticated
def patch(name):
    """Modifies an account."""

    if name == '!':
        return patch_user(ACCOUNT)

    account = account_by_name(name)

    if ACCOUNT.root:
        return patch_root(account)
    elif ACCOUNT.admin and CUSTOMER == account.customer:
        return patch_admin(account)

    raise NotAuthorized()


ROUTES = (
    ('GET', '/account', list_, 'list_accounts'),
    ('GET', '/account/<name>', get, 'get_account'),
    ('POST', '/account', add, 'add_account'),
    ('PATCH', '/account/<name>', patch, 'patch_account'))
