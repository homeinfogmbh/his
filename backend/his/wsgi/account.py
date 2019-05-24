"""Account management."""

from peeweeplus import PasswordTooShortError
from wsgilib import JSON

from his.api import authenticated
from his.contextlocals import ACCOUNT, CUSTOMER, JSON_DATA
from his.crypto import genpw
from his.exceptions import AccountExistsError, AmbiguousDataError
from his.messages.account import ACCOUNT_CREATED
from his.messages.account import ACCOUNT_EXISTS
from his.messages.account import ACCOUNT_PATCHED
from his.messages.account import ACCOUNTS_EXHAUSTED
from his.messages.account import NO_SUCH_ACCOUNT
from his.messages.account import NOT_AUTHORIZED
from his.messages.account import PASSWORD_TOO_SHORT
from his.messages.customer import CUSTOMER_NOT_CONFIGURED
from his.messages.data import AMBIGUOUS_DATA
from his.messages.data import MISSING_DATA
from his.orm import Account, CustomerSettings


__all__ = ['get_account', 'ROUTES']


_USER_FIELDS = {'fullName', 'passwd', 'email'}
_ADMIN_FIELDS = {'name', 'fullName', 'passwd', 'email', 'admin'}


def get_account(name):
    """Safely returns the respective account."""

    if name == '!':
        return Account.get(Account.name == ACCOUNT.name)

    if ACCOUNT.root:
        try:
            return Account.get(Account.name == name)
        except Account.DoesNotExist:
            raise NO_SUCH_ACCOUNT

    try:
        account = Account.get(Account.name == name)
    except Account.DoesNotExist:
        raise NOT_AUTHORIZED    # Prevent account name sniffing.

    if ACCOUNT.admin:
        if account.customer == CUSTOMER:
            return account
    elif ACCOUNT.name == account.name and ACCOUNT.id == account.id:
        return account

    raise NOT_AUTHORIZED


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
        raise MISSING_DATA.update(missing_fields=missing_fields)

    try:
        account = Account.add(CUSTOMER, name, email, passwd=passwd)
    except AccountExistsError:
        raise ACCOUNT_EXISTS
    except PasswordTooShortError as password_too_short:
        raise PASSWORD_TOO_SHORT.update(minlen=password_too_short.minlen)

    account.save()

    if password_generated:
        return ACCOUNT_CREATED.update(passwd=passwd)

    return ACCOUNT_CREATED


def _patch_account(account, only=None):
    """Patches the respective account with the provided
    dictionary and an optional field restriction.
    """

    try:
        account.patch_json(JSON_DATA, only=only)
    except PasswordTooShortError as password_too_short:
        raise PASSWORD_TOO_SHORT.update(minlen=password_too_short.minlen)
    except AmbiguousDataError as error:
        raise AMBIGUOUS_DATA.update(field=str(error))

    account.save()
    return ACCOUNT_PATCHED


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
            return CUSTOMER_NOT_CONFIGURED

        if settings.max_accounts is None:
            return _add_account()

        accounts = sum(1 for _ in Account.select().where(
            Account.customer == CUSTOMER))

        if accounts < settings.max_accounts:
            return _add_account()

        return ACCOUNTS_EXHAUSTED

    return NOT_AUTHORIZED


@authenticated
def patch(name):
    """Modifies an account."""

    account = get_account(name)

    if ACCOUNT.root:
        return _patch_account(account)

    if ACCOUNT.admin and CUSTOMER == account.customer:
        return _patch_account(account, only=_ADMIN_FIELDS)

    if ACCOUNT.id == account.id:
        return _patch_account(account, only=_USER_FIELDS)

    return NOT_AUTHORIZED


ROUTES = (
    ('GET', '/account', list_),
    ('GET', '/account/<name>', get),
    ('POST', '/account', add),
    ('PATCH', '/account/<name>', patch)
)
