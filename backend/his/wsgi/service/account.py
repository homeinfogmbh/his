"""Account <> Service mappings."""

from wsgilib import JSON

from his.api import authenticated, admin
from his.exceptions import InconsistencyError
from his.globals import ACCOUNT, JSON_DATA
from his.messages.account import NoAccountSpecified
from his.messages.account import NotAuthorized
from his.messages.service import AccountServiceDeleted
from his.messages.service import NoServiceSpecified
from his.messages.service import NoSuchAccountService
from his.messages.service import ServiceAdded
from his.orm import AccountService
from his.wsgi.account import get_account
from his.wsgi.service.functions import get_service


__all__ = ['ROUTES']


@authenticated
def list_():
    """Lists services of the respective account."""

    return JSON([
        account_service.service.to_json() for account_service
        in AccountService.select().where(
            AccountService.account == ACCOUNT.id)])


@authenticated
@admin
def add():
    """Allows the respective account to use the given service."""

    try:
        account = get_account(JSON_DATA['account'])
    except KeyError:
        return NoAccountSpecified()

    if account not in ACCOUNT.subjects:
        return NotAuthorized()

    try:
        service = get_service(JSON_DATA['service'])
    except KeyError:
        return NoServiceSpecified()

    try:
        account.services.add(service)
    except InconsistencyError:
        return NotAuthorized()

    return ServiceAdded()


@authenticated
@admin
def delete(name):
    """Deletes the respective account <> service mapping."""

    service = get_service(name)

    try:
        account_service = AccountService.get(
            (AccountService.account == ACCOUNT.id)
            & (AccountService.service == service))
    except AccountService.DoesNotExist:
        return NoSuchAccountService()

    account_service.delete_instance()
    return AccountServiceDeleted()


ROUTES = (
    ('POST', '/service/account', add, 'add_account_service'),
    ('GET', '/service/account', list_, 'list_account_services'),
    ('DELETE', '/service/account/<name>', delete, 'delete_account_service'))
