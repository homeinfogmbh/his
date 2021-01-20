"""HIS configuration."""

from configparser import ConfigParser
from json import load


__all__ = ['CONFIG', 'CORS', 'RECAPTCHA']


CONFIG = ConfigParser()
CONFIG.read('his.d/his.conf')

with open('his.d/cors.json', 'r') as file:
    CORS = load(file)

with open('his.d/recaptcha.json', 'r') as file:
    RECAPTCHA = load(file)
