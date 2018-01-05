"""HIS WSGI core services."""

from itertools import chain

from wsgilib import Application

from his.wsgi import account, customer, service, session

__all__ = ['APPLICATION']


APPLICATION = Application('his', debug=True, cors=True)
APPLICATION.set_endpoint('account', account.ROUTES)
APPLICATION.set_endpoint('customer', customer.ROUTES)
APPLICATION.set_endpoint('service', service.ROUTES)
APPLICATION.set_endpoint('session', session.ROUTES)
