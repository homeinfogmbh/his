"""Account <> Service mappings."""

from wsgilib import JSON, JSONMessage

from his.api import authenticated, admin
from his.contextlocals import ACCOUNT, JSON_DATA
from his.exceptions import InconsistencyError
from his.messages.account import NO_ACCOUNT_SPECIFIED
from his.messages.account import NOT_AUTHORIZED
from his.messages.service import ACCOUNT_SERVICE_DELETED
from his.messages.service import NO_SERVICE_SPECIFIED
from his.messages.service import NO_SUCH_ACCOUNT_SERVICE
from his.messages.service import SERVICE_ADDED
from his.orm import AccountService
from his.wsgi.account import get_account
from his.wsgi.service.functions import get_service


__all__ = ['ROUTES']


@authenticated
def list_() -> JSON:
    """Lists services of the respective account."""

    return JSON([
        account_service.service.to_json() for account_service
        in AccountService.select().where(
            AccountService.account == ACCOUNT.id)])


@authenticated
@admin
def add() -> JSONMessage:
    """Allows the respective account to use the given service."""

    try:
        account = get_account(JSON_DATA['account'])
    except KeyError:
        return NO_ACCOUNT_SPECIFIED

    if account not in ACCOUNT.subjects:
        return NOT_AUTHORIZED

    try:
        service = get_service(JSON_DATA['service'])
    except KeyError:
        return NO_SERVICE_SPECIFIED

    try:
        account.services.add(service)
    except InconsistencyError:
        return NOT_AUTHORIZED

    return SERVICE_ADDED


@authenticated
@admin
def delete(name: str) -> JSONMessage:
    """Deletes the respective account <> service mapping."""

    service = get_service(name)

    try:
        account_service = AccountService.get(
            (AccountService.account == ACCOUNT.id)
            & (AccountService.service == service))
    except AccountService.DoesNotExist:
        return NO_SUCH_ACCOUNT_SERVICE

    account_service.delete_instance()
    return ACCOUNT_SERVICE_DELETED


ROUTES = (
    ('POST', '/service/account', add),
    ('GET', '/service/account', list_),
    ('DELETE', '/service/account/<name>', delete)
)
