"""ORM model proxies."""

from his.exceptions import InconsistencyError


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
    def account_service_model(self):
        """Returns the AccountService model."""
        return self.account.account_services.model

    @property
    def customer_service_model(self):
        """Returns the CustomerService model."""
        return self.account.customer.customer_services.model

    @property
    def services(self):
        """Yields directly assigned services."""
        account_service_model = self.account_service_model

        for account_service in account_service_model.select().where(
                account_service_model.account == self.account):
            yield account_service.service

    def add(self, service):
        """Maps a service to this account."""
        account_service_model = self.account_service_model

        if service in self.services:
            return False

        if service in self.customer_service_model.services(
                self.account.customer):
            account_service = account_service_model()
            account_service.account = self.account
            account_service.service = service
            account_service.save()
            return True

        raise InconsistencyError(
            'Cannot enable service {} for account {}, because the '
            'respective customer {} is not enabled for it.'.format(
                service, self.account, self.account.customer))

    def remove(self, service):
        """Removes a service from the account's mapping."""
        account_service_model = self.account_service_model

        for account_service in account_service_model.select().where(
                (account_service_model.account == self.account) &
                (account_service_model.service == service)):
            account_service.delete_instance()
