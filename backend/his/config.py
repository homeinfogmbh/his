"""HIS configuration."""

from configlib import loadcfg, JSONParser


__all__ = ['CONFIG', 'PWRESET']


CONFIG = loadcfg('his.d/his.conf')
PWRESET = JSONParser('/usr/local/etc/his.d/pwreset.json')
