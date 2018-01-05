"""HIS WSGI core services."""

from wsgilib import Application

from his.wsgi import account, customer, service, session

__all__ = ['APPLICATION']

ENDPOINTS = {}
ENDPOINTS.update(account.ENDPOINTS)
ENDPOINTS.update(customer.ENDPOINTS)
ENDPOINTS.update(service.ENDPOINTS)
ENDPOINTS.update(session.ENDPOINTS)
APPLICATION = Application('his', debug=True, cors=True)
APPLICATION.add_endpoints(ENDPOINTS)
