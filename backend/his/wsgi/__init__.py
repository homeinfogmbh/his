"""HIS WSGI core services."""

from his.application import Application
from his.config import CORS
from his.wsgi import account, bugreport, customer, pwreset, service, session


__all__ = ['APPLICATION']


APPLICATION = Application('his', debug=True, cors=CORS)
APPLICATION.add_routes(
    account.ROUTES + bugreport.ROUTES + customer.ROUTES + pwreset.ROUTES
    + service.ROUTES + session.ROUTES)
