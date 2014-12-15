"""
Defines the HIS service template
"""
from .resource import Resource

__date__ = '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase', 'Service']


class Service(Resource):
    """Common service class"""
    def __init__(self):
        """Initializes relative to parent resource"""
        super().__init__(None)

    @property
    def resources(self):
        """Returns a generator of all the service's resources"""
        for attr in dir(self):
            if type(attr) is Resource:
                yield getattr(self, attr)
