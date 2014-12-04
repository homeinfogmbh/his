"""
Abstract base classes for HIS's views
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '04.12.2014'
__all__ = ['Resource']


class ResourceType():
    """
    An abstract, basic resource type
    """
    def __init__(self, name, requires_authentication=True,
                 requires_authorization=False, administrative=False):
        """Initializes the resource's path and protection flag"""
        self.__name = name
        self.__requires_authentication = requires_authentication
        self.__requires_authorization = requires_authorization
        self.__administrative = administrative

    @property
    def name(self):
        """Returns the resource's name"""
        return self.__name

    @property
    def requires_authentication(self):
        """Returns whether the resource requires authentication"""
        return self.__requires_authentication

    @property
    def requires_authorization(self):
        """Returns whether the resource requires authorization"""
        return self.__requires_authorization

    @property
    def administrative(self):
        """Returns whether the resource requires administrative privileges"""
        return self.__administrative


class Resource():
    """
    HISs' resources
    """
    OVERVIEW = ResourceType('overview',
                            requires_authentication=True,
                            requires_authorization=True,
                            administrative=False)
    COMPANY_PREFS = ResourceType('company',
                                 requires_authentication=True,
                                 requires_authorization=True,
                                 administrative=True)
    USER_PREFS = ResourceType('user',
                              requires_authentication=True,
                              requires_authorization=True,
                              administrative=False)
    PREVIEWS = ResourceType('preview',
                            requires_authentication=False,
                            requires_authorization=False,
                            administrative=False)
    SERVICES = ResourceType('service',
                            requires_authentication=True,
                            equires_authorization=True,
                            administrative=False)
