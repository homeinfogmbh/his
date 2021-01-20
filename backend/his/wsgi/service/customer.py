"""Customer <> Service mappings."""

from flask import request

from wsgilib import JSON, JSONMessage

from his.api import authenticated, root, admin
from his.contextlocals import CUSTOMER
from his.decorators import require_json
from his.orm.customer_service import CustomerService
from his.wsgi.functions import get_customer
from his.wsgi.functions import get_customer_service
from his.wsgi.functions import get_customer_services
from his.wsgi.functions import get_service


__all__ = ['ROUTES']


@authenticated
@admin
def list_() -> JSON:
    """Lists services of the respective customer."""

    return JSON([cs.to_json() for cs in get_customer_services(CUSTOMER.id)])


@authenticated
@root
@require_json(dict)
def add() -> JSONMessage:
    """Allows the respective customer to use the given service."""

    customer = get_customer(request.json['customer'])
    service = get_service(request.json['service'])
    customer_service = CustomerService.add(customer, service)
    return JSONMessage('Customer service added.', id=customer_service.id,
                       status=201)


@authenticated
@admin
def delete(name: str) -> JSONMessage:
    """Deletes the respective account <> service mapping."""

    service = get_service(name)
    customer_service = get_customer_service(CUSTOMER.id, service)
    customer_service.delete_instance()
    return JSONMessage('Customer service deleted.', status=200)


ROUTES = [
    ('GET', '/service/customer', list_),
    ('POST', '/service/customer', add),
    ('DELETE', '/service/customer/<name>', delete)
]
