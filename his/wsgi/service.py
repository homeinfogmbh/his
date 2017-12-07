"""HIS meta services."""

from flask import request
from peewee import DoesNotExist

from homeinfo.crm import Customer

from his.api import authenticated
from his.globals import ACCOUNT, CUSTOMER
from his.messages.account import NotAuthorized, NoSuchAccount
from his.messages.customer import InvalidCustomerID, NoSuchCustomer
from his.messages.service import NoServiceSpecified, NoSuchService, \
    ServiceAdded, ServiceAlreadyEnabled, AmbiguousServiceTarget, \
    MissingServiceTarget
from his.orm import InconsistencyError, Service, CustomerService, Account
from his.wsgi import APPLICATION

__all__ = ['add_service']


def add_customer_service(customer_id, service):
    """Allows the respective customer to use the given service."""

    if not ACCOUNT.root:
        raise NotAuthorized()

    try:
        cid = int(customer_id)
    except ValueError:
        raise InvalidCustomerID()

    try:
        customer = Customer.get(Customer.id == cid)
    except DoesNotExist:
        raise NoSuchCustomer()

    try:
        CustomerService.get(
            (CustomerService.customer == customer)
            & (CustomerService.service == service))
    except DoesNotExist:
        customer_service = CustomerService()
        customer_service.customer = customer
        customer_service.service = service
        customer_service.save()
        return ServiceAdded()

    return ServiceAlreadyEnabled()


def add_account_service(account_name, service):
    """Allows the respective account to use the given service."""

    if not ACCOUNT.admin:
        raise NotAuthorized()

    try:
        account = Account.get(Account.name == account_name)
    except DoesNotExist:
        raise NoSuchAccount()

    if CUSTOMER != account.customer:
        raise NotAuthorized()

    try:
        account.services.add(service)
    except InconsistencyError:
        raise NotAuthorized()

    return ServiceAdded()


@APPLICATION.route('/service', methods=['POST'])
@authenticated
def add_service():
    """Adds the respective service."""

    try:
        service = Service.get(Service.name == request.args['service'])
    except KeyError:
        raise NoServiceSpecified()
    except DoesNotExist:
        raise NoSuchService()

    customer_id = request.args.get('customer')
    account_name = request.args.get('account')

    if customer_id is not None and account_name is not None:
        raise AmbiguousServiceTarget()
    elif customer_id is not None:
        return add_customer_service(customer_id, service)
    elif account_name is not None:
        return add_account_service(account_name, service)

    raise MissingServiceTarget()
