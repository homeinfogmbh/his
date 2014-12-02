"""
Models for the HOMEINFO Integrated Services
"""
from .passwd import User, Group
from .service import Service, UserService, GroupService

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '16.10.2014'
__all__ = ['User', 'Group']
__tables__ = [User, Group, Service, UserService, GroupService]
"""The actual databases's tables"""
