"""HIS configuration."""

from configlib import INIParser, JSONParser


__all__ = ['CONFIG', 'PWRESET']


CONFIG = INIParser('/etc/his.d/his.conf')
PWRESET = JSONParser('/etc/his.d/pwreset.json', alert=True)
