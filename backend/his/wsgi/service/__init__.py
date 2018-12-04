"""Service end points."""

from his.wsgi.service.account import ROUTES as ACCOUNT_ROUTES
from his.wsgi.service.customer import ROUTES as CUSTOMER_ROUTES
from his.wsgi.service.service import ROUTES as SERVICE_ROUTES
from his.wsgi.service.functions import get_service


__all__ = ['ROUTES', 'get_service']


ROUTES = ACCOUNT_ROUTES + CUSTOMER_ROUTES + SERVICE_ROUTES
