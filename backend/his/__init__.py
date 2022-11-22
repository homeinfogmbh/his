"""HOMEINFO Integrated Services.

HOMEINFO's SSO web service framework.
"""
from his.api import authenticated, authorized, admin, root
from his.application import Application
from his.config import get_cors
from his.contextlocals import ACCOUNT, CUSTOMER, SESSION
from his.crypto import genpw
from his.functions import stakeholders
from his.mail import get_mailer
from his.orm import Account, AccountService, CustomerService, Service
from his.parsers import account, service


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'SESSION',
    'Application',
    'Account',
    'AccountService',
    'CustomerService',
    'Service',
    'account',
    'authenticated',
    'authorized',
    'admin',
    'genpw',
    'get_cors',
    'get_mailer',
    'root',
    'service',
    'stakeholders'
]
