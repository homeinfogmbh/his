"""HIS configuration"""

from configparserplus import ConfigParserPlus

__all__ = ['config']

config = ConfigParserPlus('/etc/his.d/his.conf')
