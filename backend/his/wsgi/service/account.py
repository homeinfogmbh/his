"""HIS meta services."""

from wsgilib import JSON

from his.api import authenticated, admin
from his.globals import ACCOUNT, JSON_DATA
from his.messages.account import NotAuthorized, NoAccountSpecified
from his.messages.service import NoServiceSpecified
from his.messages.service import ServiceAdded
from his.orm import AccountService
from his.orm import InconsistencyError
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


ROUTES = (
    ('POST', '/service/account', add, 'add_account_service'),
    ('GET', '/service/account', list_, 'list_account_services'))
