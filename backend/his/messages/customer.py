"""Customer related messages."""

from his.messages.facility import HIS_MESSAGE


__all__ = [
    'NO_CUSTOMER_SPECIFIED',
    'NO_SUCH_CUSTOMER',
    'CUSTOMER_NOT_CONFIGURED']


NO_CUSTOMER_SPECIFIED = HIS_MESSAGE('No customer specified.', status=420)
NO_SUCH_CUSTOMER = HIS_MESSAGE(
    'The specified customer does not exist.', status=404)
CUSTOMER_NOT_CONFIGURED = HIS_MESSAGE(
    'The specified customer has no configuration.', status=404)
