"""Customer-level meta services"""

from his.api.globals import CUSTOMER
from his.api.handlers import AdminService
from his.api.messages import InvalidOperation, CustomerUnconfigured
from his.orm import CustomerSettings
from his.wsgi import APPLICATION

__all__ = ['CustomerService']


def settings(self):
    """Returns the respective customer settings."""

    try:
        CustomerSettings.get(CustomerSettings.customer == CUSTOMER)
    except DoesNotExist:
        raise CustomerUnconfigured() from None


@APPLICATION.route('/customer', methods=['GET'])
def get_customer(self):
    """Allows services"""

    return jsonify(CUSTOMER.to_dict())


@APPLICATION.route('/customer/logo', methods=['GET'])
def get_customer(self):
    """Allows services"""

    return Binary(settings().logo)
