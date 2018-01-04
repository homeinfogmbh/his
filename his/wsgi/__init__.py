"""HIS WSGI core services."""

from itertools import chain

from wsgilib import Application

from his.wsgi import account, customer, service, session

__all__ = ['APPLICATION']


APPLICATION = Application('his', debug=True, cors=True)
APPLICATION.routes_table = chain(
    account.ROUTES, customer.ROUTES, service.ROUTES, session.ROUTES)
