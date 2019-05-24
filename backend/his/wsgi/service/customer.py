"""Customer <> Service mappings."""

from wsgilib import JSON

from his.api import authenticated, root, admin
from his.contextlocals import CUSTOMER, JSON_DATA
from his.messages.customer import NO_CUSTOMER_SPECIFIED
from his.messages.service import CUSTOMER_SERVICE_DELETED
from his.messages.service import NO_SERVICE_SPECIFIED
from his.messages.service import NO_SUCH_CUSTOMER_SERVICE
from his.messages.service import SERVICE_ADDED
from his.messages.service import SERVICE_ALREADY_ENABLED
from his.orm import Service, CustomerService
from his.wsgi.customer import get_customer
from his.wsgi.service.functions import get_service


__all__ = ['ROUTES']


@authenticated
@admin
def list_():
    """Lists services of the respective customer."""

    return JSON([
        customer_service.service.to_json() for customer_service
        in CustomerService.select().where(
            CustomerService.customer == CUSTOMER.id)])


@authenticated
@root
def list_customers(name):
    """Lists the customers that may use the current service."""

    return JSON([
        customer_service.customer.to_json(company=True) for customer_service
        in CustomerService.select().join(Service).where(Service.name == name)])


@authenticated
@root
def add():
    """Allows the respective customer to use the given service."""

    try:
        customer = get_customer(JSON_DATA['customer'])
    except KeyError:
        return NO_CUSTOMER_SPECIFIED

    try:
        service = get_service(JSON_DATA['service'])
    except KeyError:
        return NO_SERVICE_SPECIFIED

    try:
        CustomerService.get(
            (CustomerService.customer == customer)
            & (CustomerService.service == service))
    except CustomerService.DoesNotExist:
        customer_service = CustomerService()
        customer_service.customer = customer
        customer_service.service = service
        customer_service.save()
        return SERVICE_ADDED

    return SERVICE_ALREADY_ENABLED


@authenticated
@admin
def delete(name):
    """Deletes the respective account <> service mapping."""

    service = get_service(name)

    try:
        customer_service = CustomerService.get(
            (CustomerService.customer == CUSTOMER.id)
            & (CustomerService.service == service))
    except CustomerService.DoesNotExist:
        return NO_SUCH_CUSTOMER_SERVICE

    customer_service.delete_instance()
    return CUSTOMER_SERVICE_DELETED


ROUTES = (
    ('GET', '/service/customer', list_),
    ('GET', '/service/<name>/customers', list_customers),
    ('POST', '/service/customer', add),
    ('DELETE', '/service/customer/<name>', delete)
)
