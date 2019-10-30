"""HOMEINFO Integrated Services.

HOMEINFO's SSO web service framework.
"""
from his.api import authenticated, authorized, admin, root
from his.application import Application
from his.contextlocals import ACCOUNT, CUSTOMER, JSON_DATA, SESSION
from his.orm import Account


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'JSON_DATA',
    'SESSION',
    'authenticated',
    'authorized',
    'admin',
    'root',
    'Application',
    'Account'
]
