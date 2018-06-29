"""HIS configuration."""

from json import loads

from configlib import INIParser

__all__ = ['CONFIG', 'RECAPTCHA']


CONFIG = INIParser('/etc/his.d/his.conf')

try:
    with open('/etc/his.d/recaptcha.json') as file:
        _JSON_TEXT = file.read()
except FileNotFoundError:
    RECAPTCHA = {}
else:
    RECAPTCHA = loads(_JSON_TEXT)
