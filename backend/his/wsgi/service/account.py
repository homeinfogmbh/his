"""Account <> Service mappings."""

from flask import request

from wsgilib import JSON, JSONMessage

from his.api import authenticated, admin
from his.contextlocals import ACCOUNT
from his.errors import NOT_AUTHORIZED
from his.orm.account_service import AccountService
from his.wsgi.decorators import require_json
from his.wsgi.functions import get_account
from his.wsgi.functions import get_account_service
from his.wsgi.functions import get_account_services
from his.wsgi.functions import get_service


__all__ = ['ROUTES']


@authenticated
def list_() -> JSON:
    """Lists account services of the current account."""

    return JSON([acs.to_json() for acs in get_account_services()])


@authenticated
@admin
@require_json(dict)
def add() -> JSONMessage:
    """Allows the respective account to use the given service."""

    account = get_account(request.json.pop('account'))

    if account not in ACCOUNT.subjects:
        return NOT_AUTHORIZED

    service = get_service(request.json.pop('service'))
    account_service = AccountService.add(account, service)
    return JSONMessage('Account service added.', id=account_service.id,
                       status=200)


@authenticated
@admin
def delete(ident: int) -> JSONMessage:
    """Deletes the respective account <> service mapping."""

    get_account_service(ident).delete_instance()
    return JSONMessage('Account service deleted.', status=200)


ROUTES = [
    ('POST', '/service/account', add),
    ('GET', '/service/account', list_),
    ('DELETE', '/service/account/<int:ident>', delete)
]
