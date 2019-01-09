"""HOMEINFO Integrated Services.

The HOMEINFO Integrated Services (HIS) are a meta webservice
on top of which actual web services with centralized authentication
may be implemented.

(C) 2017: HOMEINFO - Digitale Informationssysteme GmbH
"""
from his.api import authenticated, authorized, admin, root
from his.application import Application
from his.contextlocals import ACCOUNT, CUSTOMER, JSON_DATA
from his.messages import Message
from his.orm import Account

__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'JSON_DATA',
    'authenticated',
    'authorized',
    'admin',
    'root',
    'Application',
    'Message',
    'Account']
