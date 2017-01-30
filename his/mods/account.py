"""Account management"""

from json import loads

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, OK, JSON, InternalServerError
from homeinfo.crm import Customer

from his.api.errors import NotAuthorized, NoSuchAccount, InvalidJSON, \
    NoCustomerSpecified, NoSuchCustomer
from his.api.handlers import AuthenticatedService
from his.orm import AccountExists, Account


class AccountService(AuthenticatedService):
    """Service that handles accounts"""

    @property
    def account_(self):
        """Returns the target account"""
        try:
            return Account.get(
                (Account.name == self.resource) &
                (Account.customer == self.customer))
        except DoesNotExist:
            raise NoSuchAccount() from None

    def get(self):
        """List one or many accounts"""
        account = self.account

        if self.resource is None:
            if account.root:
                if self.query.get('customer') is None:
                    return JSON([a.to_dict() for a in Account])
                else:
                    accounts = Account.select().where(
                        Account.customer == self.customer)
                    return JSON([a.to_dict() for a in accounts])
            elif account.admin:
                accounts = Account.select().where(
                    Account.customer == self.customer)
                return JSON([a.to_dict() for a in accounts])
            else:
                raise NotAuthorized() from None
        else:
            account_ = self.account_

            if account.root:
                return JSON(account_.to_dict())
            elif account.admin:
                if account.customer == account_.customer:
                    return JSON(account_.to_dict())
                else:
                    raise NotAuthorized() from None
            else:
                raise NotAuthorized() from None

    def post(self):
        """Create a new account"""
        account = self.account

        if account.root or account.admin:
            try:
                d = loads(self.data)
            except ValueError:
                raise InvalidJSON() from None
            else:
                try:
                    customer = Customer.get(Customer.id == d['customer'])
                except KeyError:
                    raise NoCustomerSpecified() from None
                except DoesNotExist:
                    raise NoSuchCustomer() from None

                try:
                    name = d['name']
                except KeyError:
                    raise Error('No name specified')

                try:
                    email = d['email']
                except KeyError:
                    raise Error('No email specified')

                try:
                    account_ = Account.add(
                        customer, name, email,
                        passwd=d.get('passwd'),
                        disabled=d.get('disabled'),
                        admin=d.get('admin'))
                except ValueError:
                    raise InternalServerError('Value error.') from None
                except AccountExists as e:
                    raise Error('Account already exists for {}.'.format(
                        e.field), status=409) from None
                else:
                    account_.save()
                    return OK()
