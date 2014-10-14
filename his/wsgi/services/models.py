'''
Created on 14.10.2014

@author: neumannr
'''
from his.db import HISModel
from peewee import TextField, CharField

class HISService(HISModel):
    """
    A Service within the HIS system
    """
    name = TextField
    """A representative name"""