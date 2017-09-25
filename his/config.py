"""HIS configuration"""

from configlib import INIParser
from filedb import FileClient

__all__ = ['CONFIG', 'FILE_CLIENT']

CONFIG = INIParser('/etc/his.d/his.conf')
FILE_CLIENT = FileClient('7958faef-01c9-4c3b-b4ef-1aecea6945c1')
