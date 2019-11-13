"""HIS configuration."""

from configlib import loadcfg


__all__ = ['CONFIG', 'COOKIE', 'CORS', 'DOMAINS', 'RECAPTCHA']


CONFIG = loadcfg('his.d/his.conf')
COOKIE = CONFIG['auth']['cookie']
DOMAINS = CONFIG['auth']['domains'].split()
CORS = loadcfg('his.d/cors.json')
RECAPTCHA = loadcfg('his.d/recaptcha.json')
