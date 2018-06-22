"""HIS meta services."""

from wsgilib import JSON

from his.api import DATA, authenticated, root, admin
from his.globals import SESSION, ACCOUNT, CUSTOMER
from his.messages.account import NotAuthorized, NoAccountSpecified
from his.messages.customer import NoCustomerSpecified
from his.messages.service import NoServiceSpecified, NoSuchService, \
    ServiceAdded, ServiceAlreadyEnabled
from his.orm import InconsistencyError, Service, CustomerService, \
    AccountService
from his.wsgi.account import account_by_name
from his.wsgi.customer import customer_by_name

__all__ = ['ROUTES']


def service_by_name(name):
    """Returns the respective service."""

    try:
        return Service.get(Service.name == name)
    except Service.DoesNotExist:
        raise NoSuchService()


@authenticated
@root
def add_customer_service():
    """Allows the respective customer to use the given service."""

    json = DATA.json

    try:
        customer = customer_by_name(json['customer'])
    except KeyError:
        raise NoCustomerSpecified()

    try:
        service = service_by_name(json['service'])
    except KeyError:
        raise NoServiceSpecified()

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

    json = DATA.json

    try:
        account = account_by_name(json['account'])
    except KeyError:
        raise NoAccountSpecified()

    if account not in ACCOUNT.subjects:
        raise NotAuthorized()

    try:
        service = service_by_name(json['service'])
    except KeyError:
        raise NoServiceSpecified()

    try:
        account.services.add(service)
    except InconsistencyError:
        raise NotAuthorized()

    return ServiceAdded()


@authenticated
def list_services():
    """Lists promoted services."""

    if SESSION.account.root:
        return JSON([service.to_dict() for service in Service])

    return JSON([service.to_dict() for service in Service.select().where(
        Service.promote == 1)])


@authenticated
@admin
def list_customer_services():
    """Lists services of the respective customer."""

    return JSON([customer_service.service.to_dict() for customer_service
                 in CustomerService.select().where(
                     CustomerService.customer == CUSTOMER.id)])


@authenticated
def list_account_services():
    """Lists services of the respective account."""

    return JSON([account_service.service.to_dict() for account_service
                 in AccountService.select().where(
                     AccountService.account == ACCOUNT.id)])


@authenticated
@root
def list_service_customers(name):
    """Lists the customers that may use the current service."""

    return JSON([
        customer_service.customer.to_dict() for customer_service
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
    ('GET', '/service/<name>', list_service_customers,
     'list_service_customers'))
