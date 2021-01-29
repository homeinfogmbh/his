"""HIS WSGI core services."""

from his.application import Application
from his.wsgi import account, bugreport, customer, pwreset, service, session


__all__ = ['APPLICATION']


APPLICATION = Application('his')
APPLICATION.add_routes(account.ROUTES)
APPLICATION.add_routes(bugreport.ROUTES)
APPLICATION.add_routes(customer.ROUTES)
APPLICATION.add_routes(pwreset.ROUTES)
APPLICATION.add_routes(service.ROUTES)
APPLICATION.add_routes(session.ROUTES)
