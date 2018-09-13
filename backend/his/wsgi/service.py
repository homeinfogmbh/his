"""HIS meta services."""

from wsgilib import JSON

from his.api import authenticated, root, admin
from his.globals import ACCOUNT, CUSTOMER, JSON_DATA
from his.messages.account import NotAuthorized, NoAccountSpecified
from his.messages.customer import NoCustomerSpecified
from his.messages.service import NoServiceSpecified, NoSuchService, \
    ServiceAdded, ServiceAlreadyEnabled
from his.orm import InconsistencyError, Service, CustomerService, \
    AccountService
from his.wsgi.account import get_account
from his.wsgi.customer import get_customer

__all__ = ['ROUTES']


def get_service(name):
    """Returns the respective service."""

    try:
        return Service.get(Service.name == name)
    except Service.DoesNotExist:
        raise NoSuchService()


@authenticated
@root
def add_customer_service():
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


@authenticated
@admin
def add_account_service():
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
def list_services():
    """Lists promoted services."""

    if ACCOUNT.root:
        return JSON([service.to_json() for service in Service])

    return JSON([service.to_json() for service in Service.select().where(
        Service.promote == 1)])


@authenticated
@admin
def list_customer_services():
    """Lists services of the respective customer."""

    return JSON([customer_service.service.to_json() for customer_service
                 in CustomerService.select().where(
                     CustomerService.customer == CUSTOMER.id)])


@authenticated
def list_account_services():
    """Lists services of the respective account."""

    return JSON([account_service.service.to_json() for account_service
                 in AccountService.select().where(
                     AccountService.account == ACCOUNT.id)])


@authenticated
@root
def list_service_customers(name):
    """Lists the customers that may use the current service."""

    return JSON([
        customer_service.customer.to_json(company=True) for customer_service
        in CustomerService.select().join(Service).where(Service.name == name)])


ROUTES = (
    ('POST', '/service/customer', add_customer_service,
     'add_customer_service'),
    ('POST', '/service/account', add_account_service, 'add_account_service'),
    ('GET', '/service', list_services, 'list_services'),
    ('GET', '/service/customer', list_customer_services,
     'list_customer_services'),
    ('GET', '/service/account', list_account_services,
     'list_account_services'),
    ('GET', '/service/<name>/customers', list_service_customers,
     'list_service_customers'))