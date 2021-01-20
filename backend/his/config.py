"""HIS configuration."""

from configparser import ConfigParser
from json import load


__all__ = ['CONFIG', 'CORS', 'RECAPTCHA', 'read']


CONFIG = ConfigParser()
CORS = {}
RECAPTCHA = {}


def read():
    """Loads the configuration from the config files."""

    CONFIG.read('his.d/his.conf')

    with open('his.d/cors.json', 'r') as file:
        cors = load(file)

    CORS.clear()
    CORS.update(cors)

    with open('his.d/recaptcha.json', 'r') as file:
        recaptcha = load(file)

    RECAPTCHA.clear()
    RECAPTCHA.update(recaptcha)
