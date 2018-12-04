"""Customer <> Service mappings."""

from wsgilib import JSON

from his.api import authenticated, root, admin
from his.globals import CUSTOMER, JSON_DATA
from his.messages.customer import NoCustomerSpecified
from his.messages.service import NoServiceSpecified
from his.messages.service import ServiceAdded
from his.messages.service import ServiceAlreadyEnabled
from his.orm import CustomerService
from his.orm import Service
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
        return NoCustomerSpecified()

    try:
        service = get_service(JSON_DATA['service'])
    except KeyError:
        return NoServiceSpecified()

    try:
        CustomerService.get(
            (CustomerService.customer == customer)
            & (CustomerService.service == service))
    except CustomerService.DoesNotExist:
        customer_service = CustomerService()
        customer_service.customer = customer
        customer_service.service = service
        customer_service.save()
        return ServiceAdded()

    return ServiceAlreadyEnabled()


ROUTES = (
    ('GET', '/service/customer', list_, 'list_customer_services'),
    ('GET', '/service/<name>/customers', list_customers,
     'list_service_customers'),
    ('POST', '/service/customer', add, 'add_customer_service'))
