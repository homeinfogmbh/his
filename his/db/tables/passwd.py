"""
Group and user definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Group', 'User']

from .abc import HISModel, Resource
from peewee import TextField, ForeignKeyField
       
class Group(Resource):
    """
    A HOMEINFO Integrated Services group
    """
    name = TextField()
    """A representative name"""
    @property
    def users(self):
        """Fetch all users that are in this group"""
        return User.select()\
            .join(GroupMembers, on=GroupMembers.member)\
            .where(GroupMembers.group == self)
            
    def adduser(self, user):
        """Add a user to the group"""
        gm = GroupMembers()
        gm.group = self
        gm.member = user
        return gm.save()
    
    def rmuser(self, user):
        """Remove user from the group"""
        if user.group == self:
            user.group = None
            user.save()
        for gm in GroupMembers.select()\
            .where(GroupMembers.group == self \
                   and GroupMembers.member == user):
            gm.delete_instance()
        

class User(Resource):
    """
    A HOMEINFO Integrated Services user
    """
    name = TextField()
    """A representative name"""
    passwd = TextField()
    """The user's login password"""
    group = ForeignKeyField(Group)
    """The primary group of the user"""
    @property
    def groups(self):
        """Fetch all users that are in this group"""
        return Group.select()\
            .join(GroupMembers, on=GroupMembers.group)\
            .where(GroupMembers.member == self)
            
    def ingroup(self, group):
        """Determine whether the user is in the group"""
        if self.group == group:
            return True
        else:
            if group in self.groups:
                return True
            else:
                return False
    
    
class GroupMembers(HISModel):
    """
    A many-to-many mapping for groups and users
    """
    group = ForeignKeyField(Group)
    member = ForeignKeyField(User)