"""Customer related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NoCustomerSpecified',
    'NoSuchCustomer',
    'CustomerUnconfigured']


class NoCustomerSpecified(HISMessage):
    """Indicates that no customer was specified."""

    STATUS = 420


class NoSuchCustomer(HISMessage):
    """Indicates that the customer does not exist."""

    STATUS = 404


class CustomerUnconfigured(HISMessage):
    """Indicates that there is no configuration
    available for the respective customer.
    """

    STATUS = 404
