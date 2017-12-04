"""HIS meta services."""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from wsgilib import Error, OK, JSON

from his.api.messages import NoServiceSpecified, NoSuchService, \
    InvalidCustomerID, NoSuchCustomer, NotAuthorized, AmbiguousTarget
from his.api.handlers import service, AuthenticatedService
from his.orm import InconsistencyError, Service, CustomerService, Account

__all__ = ['ServicePermissions']


@service('services')
class ServicePermissions(AuthenticatedService):
    """Handles service permissions."""

    def add_customer_service(self, customer_id, service):
        """Allows the respective customer to use the given service."""
        if not self.account.root:
            raise Error('You are not a root user.', status=400) from None

        try:
            cid = int(customer_id)
        except ValueError:
            raise InvalidCustomerID() from None

        try:
            customer = Customer.get(Customer.id == cid)
        except DoesNotExist:
            raise NoSuchCustomer() from None

        try:
            CustomerService.get(
                (CustomerService.customer == customer) &
                (CustomerService.service == service))
        except DoesNotExist:
            customer_service = CustomerService()
            customer_service.customer = customer
            customer_service.service = service
            customer_service.save()
            return OK('Service added for customer.')

        return OK('Service already enabled.')

    def add_account_service(self, account_name, service):
        """Allows the respective account to use the given service."""
        if not self.account.admin:
            raise NotAuthorized()

        try:
            account = Account.get(
                Account.name == account_name)
        except DoesNotExist:
            return Error('No such account.', status=400)

        try:
            account.services.add(service)
        except InconsistencyError as error:
            return Error(error.msg, status=400)

        return OK('Service added for account.')

    def add_service(self, service):
        """Sets permissions for the respective account."""
        customer_id = self.query.get('customer')
        account_name = self.query.get('account')

        if customer_id is not None and account_name is not None:
            return AmbiguousTarget()
        elif customer_id is not None:
            return self.add_customer_service(customer_id, service)
        elif account_name is not None:
            return self.add_account_service(account_name, service)

        return Error('Neither customer, nor accout specified.', status=400)

    def post(self):
        """Allows services."""
        try:
            service = Service.get(Service.name == self.query['service'])
        except KeyError:
            raise NoServiceSpecified() from None
        except DoesNotExist:
            raise NoSuchService() from None

        return self.add_service(service)
