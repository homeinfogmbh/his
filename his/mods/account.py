"""Account management"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import JSON
from homeinfo.crm import Customer

from his.api.errors import NotAuthorized, NoSuchCustomer, NoSuchAccount
from his.api.handlers import AuthenticatedService
from his.orm import Account


class AccountService(AuthenticatedService):
    """Service that handles accounts"""

    @property
    def customer_(self):
        """Returns the target customer"""
        try:
            customer, _ = self.resource.split('/')
        except ValueError:
            customer = self.resource

        try:
            return Customer.find(customer)
        except DoesNotExist:
            raise NoSuchCustomer() from None

    def get(self):
        account = self.account.root

        if self.resource is None:
            if account.root:
                return JSON({'accounts': [a.to_dict() for a in Account]})
            else:
                raise NotAuthorized() from None
        else:
            try:
                customer, account_ = self.resource.split('/')
            except ValueError:
                try:
                    customer = Customer.find(self.resource)
                except DoesNotExist:
                    raise NoSuchCustomer() from None
                else:
                    if account.root:
                        accounts = Account.select().where(
                            Account.customer == customer)
                        return JSON([a.to_dict() for a in accounts])
                    elif account.admin:
                        if account.customer == customer:
                            accounts = Account.select().where(
                                Account.customer == customer)
                            return JSON([a.to_dict() for a in accounts])
                        else:
                            raise NotAuthorized() from None
                    else:
                        raise NotAuthorized() from None
            else:
                try:
                    customer = Customer.find(customer)
                except DoesNotExist:
                    raise NoSuchCustomer() from None
                else:
                    try:
                        account_ = Account.get(
                            (Account.customer == customer) &
                            (Account.name == account_))
                    except DoesNotExist:
                        raise NoSuchAccount() from None
                    else:
                        if account.root:
                            return JSON(account_.to_dict())
                        elif account.admin:
                            if account.customer == account_.customer:
                                return JSON(account_.to_dict())
                            else:
                                raise NotAuthorized() from None
                        else:
                            raise NotAuthorized() from None
