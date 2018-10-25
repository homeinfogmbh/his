"""HIS WSGI core services."""

from his.application import Application
from his.wsgi import account, customer, pwreset, service, session

__all__ = ['APPLICATION']


APPLICATION = Application('his', debug=True)
APPLICATION.add_routes(
    account.ROUTES + customer.ROUTES + pwreset.ROUTES + service.ROUTES
    + session.ROUTES)
