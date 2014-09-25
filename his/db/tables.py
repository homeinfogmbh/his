"""
Database tables
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

from .config import CreamModel
from peewee import TextField, DateTimeField, BooleanField, ForeignKeyField
    
#===============================================================================
# OAuth 2.0 entities
#===============================================================================
class Consumer(CreamModel):
    """
    An OAuth version 2.0 consumer
    """
    name = TextField()              # A unique name
    cid = TextField()               # The Consumer's OAuth 2.0 identifier
    secret = TextField()            # The consumer's OAuth 2.0 secret
    created = DateTimeField()       # Creation time stamp
    expiration = DateTimeField()    # Date of expiration
    expires = BooleanField()        # Does the consumer expire?
    enabled = BooleanField()        # Has the consumer been enabled?
    blocked = BooleanField()        # Is the consumer blocked?
    
    @property
    def disabled(self):
        """
        Alias to self.enabled field
        """
        return not self.enabled
    
    @disabled.setter
    def disabled(self, value):
        """
        Alias to self.enabled field
        """
        self.enabled = not value
        
    def enable(self):
        """
        Enable the consumer
        """
        self.enabled = True
        self.save()
        
    def disable(self):
        """
        Disable the consumer
        """
        self.enabled = False
        self.save()
        
    def block(self):
        """
        Block the customer
        """
        self.blocked = True
        self.save()
        
        
class Service(CreamModel):
    """
    Describes an OAuth-protected web-service
    """
    name = TextField()              # A unique name
    base_url = TextField()          # The OAuth 2.0 Base URL
    authorize_url = TextField()     # The OAuth 2.0 Authorize URL
    access_token_url = TextField()  # The OAuth 2.0 Access Token URL
    
    
class ConsumerService(CreamModel):
    """
    Many-to-many mapping for Consumers and Services
    """
    consumer = ForeignKeyField(Consumer)    # The related consumer
    service = ForeignKeyField(Service)      # The related service