"""HIS configuration."""

from configparser import ConfigParser
from json import load

from peeweeplus import MySQLDatabase


__all__ = ['CONFIG', 'CORS', 'RECAPTCHA', 'read']


CONFIG = ConfigParser()
CORS = {}
DATABASE = MySQLDatabase(None)
RECAPTCHA = {}


def read():
    """Reads the configuration file."""

    CONFIG.read('/usr/local/etc/his.d/his.conf')
    DATABASE.load_config(CONFIG['db'])
    CORS.clear()

    with open('/usr/local/etc/his.d/cors.json', 'r') as file:
        CORS.update(load(file))

    RECAPTCHA.clear()

    with open('/usr/local/etc/his.d/recaptcha.json', 'r') as file:
        RECAPTCHA.update(load(file))
