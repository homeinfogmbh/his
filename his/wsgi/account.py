"""Account management."""

from flask import request, jsonify
from peewee import DoesNotExist

from wsgilib import crossdomain, JSON

from his.api import DATA, authenticated
from his.globals import ACCOUNT, CUSTOMER, SU_CUSTOMER
from his.messages.account import NoSuchAccount, NotAuthorized, AccountExists, \
    AccountCreated, AccountPatched, AccountsExhausted
from his.messages.customer import CustomerUnconfigured
from his.messages.data import DataError, MissingData, InvalidData
from his.orm import AccountExists as AccountExists_, AmbiguousDataError, \
    Account, CustomerSettings
from his.wsgi.customer import customer_by_cid

__all__ = ['list_accounts', 'get_account', 'add_account', 'patch_account']


def account_by_name(name_or_id):
    """Returns the respective account by its name."""

    try:
        ident = int(name_or_id)
    except ValueError:
        try:
            return Account.get(Account.name == name_or_id)
        except DoesNotExist:
            raise NoSuchAccount()

    try:
        return Account.get(Account.id == ident)
    except DoesNotExist:
        raise NoSuchAccount()


def list_accounts_root():
    """Lists accounts."""

    try:
        customer = request.args['customer']
    except KeyError:
        return Account

    return Account.select().where(
        Account.customer == customer_by_cid(customer))


def _add_account():
    """Adds an account for the current customer."""

    json = DATA.json

    try:
        name = json['name']
    except KeyError:
        raise MissingData(field='name')

    try:
        email = json['email']
    except KeyError:
        raise MissingData(field='email')

    try:
        passwd = json['passwd']
    except KeyError:
        raise MissingData(field='passwd')

    try:
        account = Account.add(SU_CUSTOMER, name, email, passwd=passwd)
    except AccountExists_:
        raise AccountExists()

    account.save()
    return AccountCreated()


def _patch_account_root(account):
    """Patches the account from a root user context."""

    try:
        account.patch(DATA.json)
        account.save()
    except (TypeError, ValueError):
        raise InvalidData()
    except AmbiguousDataError as error:
        raise DataError(field=str(error))

    return AccountPatched()


def _patch_account_admin(account):
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

    if invalid_keys:
        return AccountPatched(invalid_keys=invalid_keys)

    return AccountPatched()


def _patch_account_user(account):
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


def _patch_account(account):
    """Change account data."""

    if ACCOUNT.root:
        return _patch_account_root(account)
    elif ACCOUNT.admin:
        if account.customer == CUSTOMER:
            return _patch_account_admin(account)

        raise NotAuthorized()

    if account == ACCOUNT:
        return _patch_account_user(account)

    raise NotAuthorized()


@crossdomain(origin='*')
@authenticated
def list_accounts():
    """List one or many accounts."""

    if ACCOUNT.root:
        return JSON([account.to_dict() for account in list_accounts_root()])
    elif ACCOUNT.admin:
        return JSON([account.to_dict() for account in Account.select().where(
            Account.customer == CUSTOMER)])

    raise NotAuthorized()


@crossdomain(origin='*')
@authenticated
def get_account(name):
    """Gets an account by name."""

    if name == '!':
        # Return the account of the current session.
        return jsonify(ACCOUNT.to_dict())

    account = account_by_name(name)

    if ACCOUNT.root:
        return jsonify(account.to_dict())
    elif ACCOUNT.admin:
        if account.customer == CUSTOMER:
            return jsonify(account.to_dict())

        raise NotAuthorized()
    elif ACCOUNT == account:
        return jsonify(account.to_dict())

    raise NotAuthorized()


@crossdomain(origin='*')
@authenticated
def add_account():
    """Create a new account."""

    if ACCOUNT.root:
        return _add_account()
    elif ACCOUNT.admin:
        try:
            settings = CustomerSettings.get(
                CustomerSettings.customer == CUSTOMER)
        except DoesNotExist:
            raise CustomerUnconfigured()

        if settings.max_accounts is None:
            return _add_account()

        accounts = sum(1 for _ in Account.select().where(
            Account.customer == CUSTOMER))

        if accounts < settings.max_accounts:
            return _add_account()

        raise AccountsExhausted()

    raise NotAuthorized()


@crossdomain(origin='*')
@authenticated
def patch_account(name):
    """Modifies an account."""

    if name == '!':
        return _patch_account(ACCOUNT)

    account = account_by_name(name)

    if ACCOUNT.root:
        return _patch_account(account)
    elif ACCOUNT.admin and CUSTOMER == account.customer:
        return _patch_account(account)

    raise NotAuthorized()
