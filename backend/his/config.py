"""HIS configuration."""

from json import loads

from configlib import INIParser, JSONParser

__all__ = ['CONFIG', 'RECAPTCHA']


CONFIG = INIParser('/etc/his.d/his.conf')
RECAPTCHA = JSONParser('/etc/his.d/recaptcha.json', alert=True)
