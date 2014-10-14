"""
Group and user definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '14.10.2014'

__all__ = ['Group', 'User']

from his.db.tables.services import Service as ServiceTable

class Service(ServiceTable):
    """
    An abstract HIS service
    """
    def __init__(self, request, environ, ):
    
    
    
        
        
class NonUniqueNameError(Exception):
    """
    Exception to indicate a non unique service name
    """