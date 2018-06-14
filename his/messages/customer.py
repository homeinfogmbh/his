"""Customer related messages."""

from his.messages.api import Message

__all__ = [
    'NoCustomerSpecified',
    'NoSuchCustomer',
    'CustomerUnconfigured']


class _CustomerMessage(Message):
    """Abstract common customer message."""

    LOCALES = '/etc/his.d/locale/his/customer.ini'


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
