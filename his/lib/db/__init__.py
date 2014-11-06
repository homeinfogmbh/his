"""
Models for the HOMEINFO Integrated Services
"""
from .passwd import User, Group, GroupMembers
from .services import Service, UserService, GroupService

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '16.10.2014'
__tables__ = [User, Group, GroupMembers, 
              Service, UserService, GroupService]
"""The actual databases's tables"""