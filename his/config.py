"""
Basic HIS system configuration
"""
from configparser import ConfigParser

__date__= '06.11.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['db']

CONFIG_FILE = '/usr/local/etc/his.conf'
config = ConfigParser()
config.read(CONFIG_FILE)
db = config['db']