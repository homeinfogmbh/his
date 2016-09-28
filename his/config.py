"""HIS configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['config']


class HISConfig(Configuration):
    """HIS's main configuration"""

    @property
    def db(self):
        self.load()
        return self['db']

    @property
    def wsgi(self):
        self.load()
        return self['wsgi']


config = Configuration('/etc/his.conf')
