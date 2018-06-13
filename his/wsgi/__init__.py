"""HIS WSGI core services."""

from itertools import chain

from his.application import Application
from his.wsgi import account, customer, pwreset, service, session

__all__ = ['APPLICATION']


APPLICATION = Application('his', debug=True, cors=True)
APPLICATION.add_routes(chain(
    account.ROUTES, customer.ROUTES, pwreset.ROUTES, service.ROUTES,
    session.ROUTES))
