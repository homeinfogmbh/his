"""HIS configuration."""

from configlib import load_ini, load_json


__all__ = ['CONFIG', 'COOKIE', 'DOMAIN', 'RECAPTCHA']


CONFIG = load_ini('his.d/his.conf')
COOKIE = CONFIG['auth']['cookie']
DOMAIN = CONFIG['auth']['domain']
RECAPTCHA = load_json('his.d/recaptcha.json')
