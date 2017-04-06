"""HIS configuration"""

from configparserplus import ConfigParserPlus

__all__ = ['config']


class HISConfig(ConfigParserPlus):
    """HIS's main configuration"""

    @property
    def db(self):
        self.load()
        return self['db']


config = HISConfig('/etc/his.conf')
