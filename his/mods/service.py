"""HIS meta services"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from wsgilib import Error, OK, JSON

from his.api.messages import NoServiceSpecified, NoSuchService, \
    InvalidCustomerID, NoSuchCustomer, NotAuthorized
from his.api.handlers import AuthenticatedService
from his.orm import InconsistencyError, Service, CustomerService, Account

__all__ = [
    'AmbiguousTarget',
    'ServicePermissions',
    'INSTALL']


class AmbiguousTarget(JSON):
    """Indicates that the selected target is ambiguous"""

    STATUS = 400
    LOCALE = {
        'de_DE': 'Mehrdeutiges Ziel angegeben.',
        'en_US': 'Ambiguous target selected.'}


class ServicePermissions(AuthenticatedService):
    """Handles service permissions"""

    NODE = 'services'
    NAME = 'services manager'
    DESCRIPTION = 'Manages services permissions'
    PROMOTE = False

    def post(self):
        """Allows services"""
        session = self.session

        try:
            service = Service.get(Service.name == self.query['service'])
        except KeyError:
            raise NoServiceSpecified() from None
        except DoesNotExist:
            raise NoSuchService() from None
        else:
            account = session.account
            customer_id = self.query.get('customer')
            account_name = self.query.get('account')

            if customer_id is not None and account_name is not None:
                raise AmbiguousTarget() from None
            elif customer_id is not None:
                if account.root:
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
                    else:
                        return OK('Service already enabled.')
                else:
                    raise Error('You are not a root user.', status=400)
            elif account_name is not None:
                if account.admin:
                    try:
                        account = Account.get(
                            Account.name == account_name)
                    except DoesNotExist:
                        return Error('No such account.', status=400)

                    try:
                        account.services.add(service)
                    except InconsistencyError as error:
                        return Error(error.msg, status=400)
                    else:
                        return OK('Service added for account.')
                else:
                    raise NotAuthorized()
            else:
                return Error('No customer or accout specified.',
                             status=400)


INSTALL = [ServicePermissions]
