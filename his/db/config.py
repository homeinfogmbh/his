"""
Database configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '16.10.2014'

__all__ = ['database']

from peewee import MySQLDatabase

database = MySQLDatabase('his', host='mysql.homeinfo.de', 
                         user='his', passwd='3=w,&7>_u8}oO0y')