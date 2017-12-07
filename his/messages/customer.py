"""Customer related messages."""

from his.messages.common import Message

__all__ = [
    'InvalidCustomerID',
    'NoCustomerSpecified',
    'NoSuchCustomer',
    'CustomerUnconfigured']


class InvalidCustomerID(Message):
    """Base for errors regarding customers."""

    STATUS = 406


class NoCustomerSpecified(Message):
    """Indicates that no customer was specified."""

    STATUS = 420


class NoSuchCustomer(Message):
    """Indicates that the customer does not exist."""

    STATUS = 404


class CustomerUnconfigured(Message):
    """Indicates that there is no configuration
    available for the respective customer.
    """

    STATUS = 404
