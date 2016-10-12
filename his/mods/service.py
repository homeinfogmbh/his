"""HIS meta services"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, JSON

from his.api.errors import NoServiceSpecified, \
    NoSuchService, InvalidCustomerID, NoSuchCustomer, NotAuthorized
from his.api.handlers import AuthenticatedService
from his.api.locale import Language
from his.orm import InconsistencyError, Service, CustomerService, Account

__all__ = [
    'AmbiguousTarget',
    'ServicePermissions',
    'install']


class AmbiguousTarget(JSON):
    """Indicates that the selected target is ambiguous"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Mehrdeutiges Ziel angegeben.',
        Language.EN_US: 'Ambiguous target selected.'}


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
            service = Service.get(Service.name == self.params['service'])
        except KeyError:
            raise NoServiceSpecified() from None
        except DoesNotExist:
            raise NoSuchService() from None
        else:
            account = session.account
            customer_id = self.params.get('customer')
            account_name = self.params.get('account')

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

                        if customer_service.save():
                            return OK('Service added for customer.')
                        else:
                            raise Error('Could not add service.',
                                        status=500)
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
                    except InconsistencyError as e:
                        return Error(e.msg, status=400)
                    else:
                        return OK('Service added for account.')
                else:
                    raise NotAuthorized()
            else:
                return Error('No customer or accout specified.',
                             status=400)


install = [ServicePermissions]
