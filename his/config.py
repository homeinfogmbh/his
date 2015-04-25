"""HIS configuration"""

from configparser import ConfigParser

__all__ = ['db', 'wsgi']

CONFIG_FILE = '/usr/local/etc/his.conf'
config = ConfigParser()
config.read(CONFIG_FILE)
db = config['db']
wsgi = config['wsgi']
