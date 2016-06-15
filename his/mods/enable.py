"""Enable services"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, JSON

from his.api import HISService
from his.orm import InconsistencyError, AlreadyLoggedIn, CustomerService, \
    Account, Session
from his.crypto import load


class Service(HISService):
    """Handles logins"""

    def get(self):
        """Logs in the user"""
        try:
            session_token = self.query_dict['token']
        except KeyError:
            return Error('No session specified.', status=400)
        else:
            try:
                service_name = self.query_dict['service']
                service = Service.get(Service.name == service_name)
            except KeyError:
                return Error('No service specified.', status=400)
            except DoesNotExist:
                return Error('No such service.', status=400)
            else:
                customer_id = self.query_dict.get('customer')
                account_name = self.query_dict.get('account')

                if customer_id is None and account_name is None:
                    return Error('No customer or accout specified.',
                                 status=400)

                if customer_id is not None:
                    try:
                        cid = int(customer_id)
                    except ValueError:
                        return Error('Invalid customer ID.', status=400)
                    else:
                        try:
                            customer = Customer.get(Customer.id == cid)
                        except DoesNotExist:
                            return Error('No such customer.', status=400)
                        else:
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
                                    Error('Could not add service.', status=500)
                            else:
                                Error('Service already enabled.', status=400)

                if account_name is not None:
                    try:
                        account = Account.get(Account.name == account_name)
                    except DoesNotExist:
                        return Error('No such account.', status=400)
                    else:
                        try:
                            account.services.add(service)
                        except InconsistencyError as e:
                            return Error(e.msg, status=400)
                        else:
                            return OK('Service added for account.')
