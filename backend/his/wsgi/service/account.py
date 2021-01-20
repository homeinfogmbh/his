"""Account <> Service mappings."""

from wsgilib import JSON, JSONMessage

from his.api import authenticated, admin
from his.contextlocals import ACCOUNT, JSON_DATA
from his.errors import NOT_AUTHORIZED
from his.orm.account_service import AccountService
from his.wsgi.account import get_account
from his.wsgi.functions import get_account_service
from his.wsgi.functions import get_account_services
from his.wsgi.functions import get_service


__all__ = ['ROUTES']


@authenticated
def list_() -> JSON:
    """Lists account services of the current account."""

    return JSON([acs.to_json() for acs in get_account_services(ACCOUNT.id)])


@authenticated
@admin
def add() -> JSONMessage:
    """Allows the respective account to use the given service."""

    account = get_account(JSON_DATA['account'])

    if account not in ACCOUNT.subjects:
        return NOT_AUTHORIZED

    service = get_service(JSON_DATA['service'])
    account_service = AccountService.add(account, service)
    return JSONMessage('Account service added.', id=account_service.id,
                       status=200)


@authenticated
@admin
def delete(name: str) -> JSONMessage:
    """Deletes the respective account <> service mapping."""

    account_service = get_account_service(ACCOUNT.id, name)
    account_service.delete_instance()
    return JSONMessage('Account service deleted.', id=account_service.id,
                       status=200)


ROUTES = [
    ('POST', '/service/account', add),
    ('GET', '/service/account', list_),
    ('DELETE', '/service/account/<name>', delete)
]
