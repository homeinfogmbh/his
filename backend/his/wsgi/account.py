"""Account management."""

from typing import Optional

from flask import request

from wsgilib import JSON, JSONMessage

from his.api import authenticated
from his.contextlocals import ACCOUNT, CUSTOMER
from his.crypto import genpw
from his.exceptions import AccountLimitReached, NotAuthorized
from his.orm.account import Account
from his.orm.customer_settings import CustomerSettings
from his.wsgi.decorators import require_json
from his.wsgi.functions import get_account


__all__ = ['ROUTES']


USER_FIELDS = {'fullName', 'passwd', 'email'}
ADMIN_FIELDS = {'name', 'fullName', 'passwd', 'email', 'admin'}


@require_json(dict)
def add_account() -> JSONMessage:
    """Adds an account for the current customer."""

    name = request.json['name']
    email = request.json['email']
    passwd = request.json.get('passwd')
    full_name = request.json.get('fullName')

    if not passwd:
        passwd = genpw()

    if ACCOUNT.root:
        root = request.json.get('root', False)
    else:
        root = False

    if ACCOUNT.admin:
        admin = request.json.get('admin', False)
    else:
        admin = False

    account = Account.add(CUSTOMER.id, name, email, passwd,
                          full_name=full_name, admin=admin, root=root)
    return JSONMessage('Account created.', id=account.id, passwd=passwd,
                       status=201)


@require_json(dict)
def patch_account(account: Account, only: Optional[set] = None) -> JSONMessage:
    """Patches the respective account with the provided
    dictionary and an optional field restriction.
    """

    account.patch_json(request.json, only=only)
    account.save()
    return JSONMessage('Account patched.', status=200)


@authenticated
def list_() -> JSON:
    """List one or many accounts."""

    return JSON([account.to_json() for account in ACCOUNT.subjects])


@authenticated
def get(ident: Optional[int] = None) -> JSON:
    """Gets an account by name."""

    return JSON(get_account(ident).to_json())


@authenticated
def add() -> JSONMessage:
    """Create a new account."""

    if ACCOUNT.root:
        return add_account()

    if ACCOUNT.admin:
        settings = CustomerSettings.get(CustomerSettings.customer == CUSTOMER)

        if settings.max_accounts is None:
            return add_account()

        accounts = Account.select().where(Account.customer == CUSTOMER).count()

        if accounts < settings.max_accounts:
            return add_account()

        raise AccountLimitReached()

    raise NotAuthorized()


@authenticated
def patch(ident: Optional[str] = None) -> JSONMessage:
    """Modifies an account."""

    account = get_account(ident)

    if ACCOUNT.root:
        return patch_account(account)

    if ACCOUNT.admin and CUSTOMER == account.customer:
        return patch_account(account, only=ADMIN_FIELDS)

    if ACCOUNT.id == account.id:
        return patch_account(account, only=USER_FIELDS)

    raise NotAuthorized()


ROUTES = [
    ('GET', '/account', list_),
    ('GET', '/account/<int:ident>', get),
    ('GET', '/account/!', lambda: get()),   # pylint: disable=W0108
    ('POST', '/account', add),
    ('PATCH', '/account/<int:ident>', patch),
    ('PATCH', '/account/!', lambda: patch())    # pylint: disable=W0108
]
