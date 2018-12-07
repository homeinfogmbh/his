"""HIS configuration."""

from configlib import load_ini, load_json


__all__ = ['CONFIG', 'PWRESET']


CONFIG = load_ini('his.d/his.conf')
PWRESET = load_json('his.d/pwreset.json')
