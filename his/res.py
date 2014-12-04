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
    def __init__(self, parent, name, requires_authentication=True,
                 requires_authorization=False, administrative=False):
        """Initializes the resource's path and protection flag"""
        self.__parent = parent
        self.__name = name
        self.__requires_authentication = requires_authentication
        self.__requires_authorization = requires_authorization
        self.__administrative = administrative

    @property
    def parent(self):
        """Returns the resource's parent"""
        return self.__parent

    @property
    def name(self):
        """Returns the resource's name"""
        return self.__name

    @property
    def path(self):
        """Returns the resource's path"""
        '/'.join(['' if self.parent is None else self.parent.path, self.name])

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
    HIS = ResourceType(None, 'overview',
                       requires_authentication=True,
                       requires_authorization=False,
                       administrative=False)

    OVERVIEW = ResourceType(HIS, 'overview',
                            requires_authentication=True,
                            requires_authorization=False,
                            administrative=False)
    COMPANY_PREFS = ResourceType(HIS, 'company',
                                 requires_authentication=True,
                                 requires_authorization=True,
                                 administrative=True)
    USER_PREFS = ResourceType(HIS, 'user',
                              requires_authentication=True,
                              requires_authorization=True,
                              administrative=False)
    PREVIEWS = ResourceType(HIS, 'preview',
                            requires_authentication=False,
                            requires_authorization=False,
                            administrative=False)
    SERVICES = ResourceType(HIS, 'service',
                            requires_authentication=True,
                            equires_authorization=True,
                            administrative=False)
