"""Account management"""

from peewee import DoesNotExist

from homeinfo.lib.wsgi import JSON

from his.api.errors import NotAuthorized, NoSuchAccount
from his.api.handlers import AuthenticatedService
from his.orm import Account


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
        account = self.account.root

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
