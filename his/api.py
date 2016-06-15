"""Meta-services for HIS"""

from json import dumps

from homeinfo.lib.config import Configuration
from homeinfo.lib.wsgi import OK, RequestHandler

from his.config import config

__all__ = ['HISService']


class HISService(RequestHandler):
    """A generic HIS service"""

    def __init__(self, name):
        """Initializes the service handler"""
        self.name = name
        self.config_parser = Configuration(self.config_filename, alert=True)

        cors = self.config.get('CORS', 'false').lower() in ['true', '1']
        date_format = self.config.get('DEBUG')
        debug = self.config.get('DEBUG', 'false').lower() in ['true', '1']

        super().__init__(environ, cors, date_format, debug)

    @property
    def config_file_basename(self):
        return self.name + config.config['SUFFIX']

    @property
    def config_file_name(self):
        """Returns the configuration file name"""
        return join(config.config['BASEDIR'], self.config_file_basename)

    @property
    def config(self):
        """Returns the configuration section"""
        try:
            return self.config_parser[self.name]
        except KeyError:
            return {}  # Unconfigured
