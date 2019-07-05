"""HIS configuration."""

from configlib import load_ini, load_json


__all__ = ['CONFIG', 'RECAPTCHA']


CONFIG = load_ini('his.d/his.conf')
RECAPTCHA = load_json('his.d/recaptcha.json')
