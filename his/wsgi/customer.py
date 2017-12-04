"""Customer-level meta services"""

from wsgilib import JSON

from his.api.messages import InvalidOperation, CustomerUnconfigured
from his.api.handlers import AdminService
from his.orm import CustomerSettings

__all__ = ['CustomerService']


class CustomerService(AdminService):
    """Handles service permissions"""

    @property
    def settings(self):
        """Returns the respective customer settings."""
        try:
            CustomerSettings.get(CustomerSettings.customer == self.customer)
        except DoesNotExist:
            raise CustomerUnconfigured() from None

    def get(self):
        """Allows services"""
        if self.resource is not None:
            if self.resource == 'logo':
                return Binary(self.settings.logo)

            raise InvalidOperation() from None

        return JSON(self.customer.to_dict())
