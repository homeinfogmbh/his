"""HIS configuration."""

from configlib import INIParser

__all__ = ['CONFIG', 'ROOT']

CONFIG = INIParser('/etc/his.d/his.conf')

try:
    ROOT = CONFIG['wsgi']['root']
except KeyError:
    ROOT = 'his'
