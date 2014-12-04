"""
Abstract base classes for HIS's views
"""
from .abc import HISModel
from peewee import ForeignKeyField, CharField, BooleanField
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '04.12.2014'
__all__ = ['Resource']


class Resource(HISModel):
    """
    An abstract, basic resource type
    """
    name = CharField(16)
    """The resource's name"""
    parent = ForeignKeyField('self', related_name='children',
                             db_column='parent')
    """The resource's parent"""
    requires_authentication = BooleanField()
    """Does the resource require authentication (= login, session)"""
    requires_authorization = BooleanField()
    """Does the resource require authorization (= buying the service)"""
    administrative = BooleanField()
    """Does the user need administrative
    permissions to modify the resource"""
    super_admin = BooleanField()
    """Does the user need super-administrative
    permissions to modify the resource"""

    @property
    def path(self):
        """Returns the resource's path"""
        return '/'.join([self.parent.path if self.parent else '', self.name])

    @classmethod
    def add(cls, name, parent=None,
            requires_authentication=True,
            requires_authorization=True,
            administrative=False,
            super_admin=False):
        for resource in cls.select().limit(1).where(cls.name == name):
            return resource
        else:
            resource = cls()
            resource.name = name
            resource.parent = parent
            resource.requires_authentication = requires_authentication
            resource.requires_authorization = requires_authorization
            resource.administrative = administrative
            resource.super_admin = super_admin
            resource.save()
            return resource


class InitResources():
    """
    HISs' resources
    """
    HIS = Resource.add('his',
                       requires_authentication=True,
                       requires_authorization=False,
                       administrative=False)

    OVERVIEW = Resource.add('overview', parent=HIS,
                            requires_authentication=True,
                            requires_authorization=False,
                            administrative=False)
    COMPANY_PREFS = Resource.add('company', parent=HIS,
                                 requires_authentication=True,
                                 requires_authorization=True,
                                 administrative=True)
    USER_PREFS = Resource.add('user', parent=HIS,
                              requires_authentication=True,
                              requires_authorization=True,
                              administrative=False)
    PREVIEWS = Resource.add('preview', parent=HIS,
                            requires_authentication=False,
                            requires_authorization=False,
                            administrative=False)
    SERVICES = Resource.add('service', parent=HIS,
                            requires_authentication=True,
                            requires_authorization=True,
                            administrative=False)
