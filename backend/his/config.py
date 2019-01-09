"""HIS configuration."""

from configlib import load_ini, load_json


__all__ = ['CONFIG', 'DOMAIN', 'PWRESET']


CONFIG = load_ini('his.d/his.conf')
PWRESET = load_json('his.d/pwreset.json')
DOMAIN = '.homeinfo.de'
