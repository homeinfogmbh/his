"""Customer-level meta services"""

from his.api.handlers import AdminService

__all__ = ['Logo']


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
