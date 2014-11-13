"""
Group and user definitions
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '09.10.2014'

__all__ = ['Group', 'User', 'GroupMembers']

from .abc import HISModel
from homeinfo.crm import Customer
from peewee import ForeignKeyField, CharField, IntegerField, BooleanField


class Group(HISModel):
    """
    A HOMEINFO Integrated Services group
    """
    cid = IntegerField()
    """Customer identifier of the corresponding customer"""
    name = CharField(64)
    """A representative name"""
    @property
    def users(self):
        """Fetch all users that are in this group"""
        return (User.select()
                .join(GroupMembers, on=GroupMembers.member)
                .where(GroupMembers.group == self))

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
        for gm in (GroupMembers.select()
                   .where(GroupMembers.group == self
                          and GroupMembers.member == user)):
            gm.delete_instance()

    @property
    def customer(self):
        """Returns the corresponding customer"""
        return Customer.select.where(Customer.cid == self.cid)

    @customer.setter
    def customer(self, customer):
        """Sets the corresponding customer"""
        self.cid = customer.cid


class User(HISModel):
    """
    A HOMEINFO Integrated Services user
    """
    name = CharField(64)
    """A representative name"""
    sha512passwd = CharField(128)
    """The user's encrypted login password"""
    group = ForeignKeyField(Group)
    """The primary group of the user"""
    logged_in = BooleanField()
    """A token to indicate and verify a running session"""

    @property
    def passwd(self):
        """Returns the user's password"""
        return self.sha512passwd

    @passwd.setter
    def passwd(self, passwd):
        """Sets the password"""
        self.sha512passwd = passwd

    @property
    def groups(self):
        """Fetch all users that are in this group"""
        return (Group.select()
                .join(GroupMembers, on=GroupMembers.group)
                .where(GroupMembers.member == self))

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
