"""Service end points."""

from his.wsgi.service.account import ROUTES as ACCOUNT_ROUTES
from his.wsgi.service.customer import ROUTES as CUSTOMER_ROUTES
from his.wsgi.service.service import ROUTES as SERVICE_ROUTES


__all__ = ["ROUTES"]


ROUTES = (*ACCOUNT_ROUTES, *CUSTOMER_ROUTES, *SERVICE_ROUTES)
