"""HIS configuration"""

from configlib import INIParser

__all__ = ['config']

config = INIParser('/etc/his.d/his.conf')
