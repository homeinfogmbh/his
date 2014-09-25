"""
Database configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'

__all__ = ['deferred_db']

from peewee import MySQLDatabase

deferred_db = MySQLDatabase()