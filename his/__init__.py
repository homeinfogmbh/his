"""HOMEINFO Integrated Services.


The HOMEINFO Integrated Services (HIS) are a meta webservice
on top of which actual web services with centralized authentication
may be implemented.

(C) 2017: HOMEINFO - Digitale Informationssysteme GmbH
"""
from his.globals import SESSION, ACCOUNT, CUSTOMER, SU_ACCOUNT, SU_CUSTOMER
from his.api import DATA, authenticated, authorized, admin, root

__all__ = [
    'SESSION',
    'ACCOUNT',
    'CUSTOMER',
    'SU_ACCOUNT',
    'SU_CUSTOMER',
    'DATA',
    'authenticated',
    'authorized',
    'admin',
    'root']
