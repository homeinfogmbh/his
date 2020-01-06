"""HIS configuration."""

from configlib import loadcfg


__all__ = [
    'CONFIG',
    'SESSION_ID',
    'SESSION_SECRET',
    'CORS',
    'DOMAINS',
    'RECAPTCHA'
]


CONFIG = loadcfg('his.d/his.conf')
SESSION_ID = CONFIG['auth']['session-id']
SESSION_SECRET = CONFIG['auth']['session-secret']
DOMAINS = CONFIG['auth']['domains'].split()
CORS = loadcfg('his.d/cors.json')
RECAPTCHA = loadcfg('his.d/recaptcha.json')
