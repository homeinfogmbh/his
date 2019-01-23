"""Customer related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NO_CUSTOMER_SPECIFIED',
    'NO_SUCH_CUSTOMER',
    'CUSTOMER_NOT_CONFIGURED']


NO_CUSTOMER_SPECIFIED = HISMessage('No customer specified.', status=420)
NO_SUCH_CUSTOMER = HISMessage(
    'The specified customer does not exist.', status=404)
CUSTOMER_NOT_CONFIGURED = HISMessage(
    'The specified customer has no configuration.', status=404)
