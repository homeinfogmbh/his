"""HIS configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['homie_config']


class HISConfig(Configuration):
    """HIS's main configuration"""

    @property
    def crypto(self):
        self.load()
        return self['crypto']

    @property
    def db(self):
        self.load()
        return self['db']

    @property
    def wsgi(self):
        self.load()
        return self['wsgi']


his_config = HISConfig('/etc/his.conf')
