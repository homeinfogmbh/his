"""HIS configuration."""

from configlib import INIParser

__all__ = ['CONFIG']

CONFIG = INIParser('/etc/his.d/his.conf')
