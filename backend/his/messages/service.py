"""Service related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NO_SERVICE_SPECIFIED',
    'NO_SUCH_SERVICE',
    'SERVICE_ADDED',
    'SERVICE_ALREADY_ENABLED',
    'AMBIGUOUS_SERVICE_TARGET',
    'MISSING_SERVICE_TARGET',
    'NO_SUCH_ACCOUNT_SERVICE',
    'ACCOUNT_SERVICE_DELETED',
    'NO_SUCH_CUSTOMER_SERVICE',
    'CUSTOMER_SERVICE_DELETED']


NO_SERVICE_SPECIFIED = HISMessage('No service specified.', status=406)
NO_SUCH_SERVICE = HISMessage('Specified service does not exist.', status=404)
SERVICE_ADDED = HISMessage('The service has been added.', status=201)
SERVICE_ALREADY_ENABLED = HISMessage(
    'The service is already enabled.', status=409)
AMBIGUOUS_SERVICE_TARGET = HISMessage(
    'The specified service target is ambiguous.', status=406)
MISSING_SERVICE_TARGET = HISMessage('No service target specified.', status=406)
NO_SUCH_ACCOUNT_SERVICE = HISMessage(
    'No such service for specified account.', status=404)
ACCOUNT_SERVICE_DELETED = HISMessage(
    'The account service has been deleted.', status=200)
NO_SUCH_CUSTOMER_SERVICE = HISMessage(
    'No such service for specified customer.', status=404)
CUSTOMER_SERVICE_DELETED = HISMessage(
    'The customer service has been deleted.', status=200)
