"""Customer-level meta services"""

from homeinfo.lib.wsgi import JSON

from his.api.errors import HISAPIError
from his.api.handlers import AdminService

__all__ = ['CustomerService']


class InvalidOperation(HISAPIError):

    ID = 600


class CustomerService(AdminService):
    """Handles service permissions"""

    def get(self):
        """Allows services"""
        if self.resource is not None:
            if self.resource == 'logo':
                # TODO: Get logo
                pass
            else:
                raise InvalidOperation() from None
        else:
            customer = self.customer
            return JSON({
                'cid': customer.cid,
                'name': customer.name})
