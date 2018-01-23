"""HOMEINFO Integrated Services.

The HOMEINFO Integrated Services (HIS) are a meta webservice
on top of which actual web services with centralized authentication
may be implemented.

(C) 2017: HOMEINFO - Digitale Informationssysteme GmbH
"""
from his.api import DATA, authenticated, authorized, admin, root
from his.globals import SESSION, ACCOUNT, CUSTOMER
from his.messages.common import locales, Message
from his.orm import his_db, Account

__all__ = [
    'SESSION',
    'ACCOUNT',
    'CUSTOMER',
    'DATA',
    'authenticated',
    'authorized',
    'admin',
    'root',
    'locales',
    'Message',
    'his_db',
    'Account']
