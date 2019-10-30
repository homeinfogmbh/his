"""Customer related messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_CUSTOMER_SPECIFIED',
    'NO_SUCH_CUSTOMER',
    'CUSTOMER_NOT_CONFIGURED'
]


NO_CUSTOMER_SPECIFIED = JSONMessage('No customer specified.', status=420)
NO_SUCH_CUSTOMER = JSONMessage(
    'The specified customer does not exist.', status=404)
CUSTOMER_NOT_CONFIGURED = JSONMessage(
    'The specified customer has no configuration.', status=404)
