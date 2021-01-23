"""HOMEINFO Integrated Services.

HOMEINFO's SSO web service framework.
"""
from his.api import authenticated, authorized, admin, root
from his.application import Application
from his.config import CORS, read
from his.contextlocals import ACCOUNT, CUSTOMER, SESSION
from his.crypto import genpw
from his.mail import get_mailer
from his.orm import Account
from his.parsers import account, service
from his.wsgi.decorators import require_json


__all__ = [
    'ACCOUNT',
    'CORS',
    'CUSTOMER',
    'SESSION',
    'Application',
    'Account',
    'account',
    'authenticated',
    'authorized',
    'admin',
    'genpw',
    'get_mailer',
    'read',
    'require_json',
    'root',
    'service'
]
