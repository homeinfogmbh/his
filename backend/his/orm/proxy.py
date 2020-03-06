"""ORM model proxies."""

from his.exceptions import InconsistencyError
from his.orm.account import AccountService, CustomerService


__all__ = ['AccountServicesProxy']


class AccountServicesProxy:
    """Proxy to transparently handle an account's services."""

    def __init__(self, account):
        """Sets the respective account."""
        self.account = account

    def __iter__(self):
        """Yields appropriate services."""
        for service in self.services:
            yield service
            yield from service.service_deps

    @property
    def services(self):
        """Yields directly assigned services."""
        for account_service in AccountService.select().where(
                AccountService.account == self.account):
            yield account_service.service

    def add(self, service):
        """Maps a service to this account."""
        if service not in self.services:
            if service in CustomerService.services(self.account.customer):
                account_service = AccountService()
                account_service.account = self.account
                account_service.service = service
                account_service.save()
                return True

            raise InconsistencyError(
                'Cannot enable service {} for account {}, because the '
                'respective customer {} is not enabled for it.'.format(
                    service, self.account, self.account.customer))

        return False

    def remove(self, service):
        """Removes a service from the account's mapping."""
        for account_service in AccountService.select().where(
                (AccountService.account == self.account) &
                (AccountService.service == service)):
            account_service.delete_instance()
