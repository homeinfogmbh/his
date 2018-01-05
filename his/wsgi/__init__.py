"""HIS WSGI core services."""

from wsgilib import Application

from his.wsgi import account, customer, service, session

__all__ = ['APPLICATION']

APPLICATION = Application('his', debug=True, cors=True)
APPLICATION.add_endpoints({
    **account.ENDPOINTS, **customer.ENDPOINTS, **service.ENDPOINTS,
    **session.ENDPOINTS})
