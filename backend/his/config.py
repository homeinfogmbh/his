"""HIS configuration."""

from configlib import loadcfg


__all__ = ['CONFIG', 'COOKIE', 'CORS', 'DOMAIN', 'RECAPTCHA']


CONFIG = loadcfg('his.d/his.conf')
COOKIE = CONFIG['auth']['cookie']
DOMAIN = CONFIG['auth']['domain']
CORS = loadcfg('his.d/cors.json')
RECAPTCHA = loadcfg('his.d/recaptcha.json')
