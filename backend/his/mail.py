"""Emailing."""

from configlib import loadcfg
from emaillib import Mailer

from his.config import CONFIG_FILE


__all__ = ['get_mailer']


def get_mailer():
    """Returns the HIS mailer."""

    config = loadcfg(CONFIG_FILE)
    return Mailer(
        config.get('mail', 'host'), config.getint('mail', 'port'),
        config.get('mail', 'user'), config.get('mail', 'passwd')
    )
