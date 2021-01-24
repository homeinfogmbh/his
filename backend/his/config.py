"""HIS configuration."""

from configlib import loadcfg


__all__ = ['CONFIG', 'CORS', 'RECAPTCHA']


CONFIG = loadcfg('his.d/his.conf')
CORS = loadcfg('his.d/cors.json')
RECAPTCHA = loadcfg('his.d/recaptcha.json')
