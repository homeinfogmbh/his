"""
Defines the HIS service databases
"""
from his.config import MASTER_DB
from playhouse.pool import PooledMySQLDatabase

__date__= '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['HISServiceDatabase']

class HISServiceDatabase(PooledMySQLDatabase):
    """A HIS service database"""
    def __init__(self, database, **kwargs):
        """Changes the name to create a '_'-separated namespace"""
        super().__init__('_'.join([MASTER_DB, database]), kwargs)