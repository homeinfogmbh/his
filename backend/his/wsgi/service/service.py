"""HIS services."""

from wsgilib import JSON

from his.api import authenticated
from his.contextlocals import ACCOUNT
from his.orm.service import Service


__all__ = ["ROUTES"]


@authenticated
def list_() -> JSON:
    """Lists promoted services."""

    select = Service.select()
    condition = True

    if not ACCOUNT.root:
        condition &= Service.promote != 0

    return JSON([service.to_json() for service in select.where(condition)])


ROUTES = [("GET", "/service", list_)]
